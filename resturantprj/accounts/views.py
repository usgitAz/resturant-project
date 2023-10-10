from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views import View
from orders.models import OrderModel
from .forms import UserForm
from .models import UserModel , UserProfileModel
from vendor.forms import VendorForm
from django.contrib import messages , auth
from .Utils import DetectUser , check_role_customer , check_role_vendor , send_verification_email , send_reset_password_email
from django.contrib.auth.decorators import login_required , user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import VendorModel
from django.template.defaultfilters import slugify
# Create your views here.


class RegisterUserView(View):
    form = UserForm()
    context={
        'form' : form
    }
    def get(self ,request):
            if request.user.is_authenticated:
                messages.info(request , "you are already logged in !")
                return redirect("myaccount")
            return render(request , 'accounts/registeruser.html', self.context)
    
    def post(self , request):
        form = UserForm(request.POST)
        if form.is_valid():
            # method one :
            password=form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role= UserModel.CUSTOMER
            form.save()
            #send email verification 
            send_verification_email(request , user)
            messages.success(request , 'Your account has been registered sucessfully ! , wait for email to activate your account.')
            return redirect('registeruser')
            #method two :
            # firstname= form.cleaned_data["first_name"]
            # lastname= form.cleaned_data["last_name"]
            # email= form.cleaned_data["email"]
            # password= form.cleaned_data["password"]
            # username= form.cleaned_data["username"]
            # #save with create user we create in models !
            # user = UserModel.objects.create_user(first_name = firstname , last_name = lastname , email=email , password=password , username=username )
            # user.role= UserModel.CUSTOMER
            # user.save()
            # return redirect('registeruser')
        

        context ={
            'form' : form
        }
        return render(request , 'accounts/registeruser.html', context)
    

class RegisterVendorView(View):
    
    def get(self ,request):
        if request.user.is_authenticated:
            messages.info(request , "you are already logged in !")
            return redirect("myaccount")
        form = UserForm
        vendorform = VendorForm

        context={
            'form' : form ,
            'vendorform' : vendorform

        }
        return render(request , 'accounts/registervendor.html' , context)
    
    def post(self , request):
        form = UserForm(request.POST)
        vendorform = VendorForm(request.POST , request.FILES)
        if form.is_valid() and vendorform.is_valid() :
            password=form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role= UserModel.VENDOR
            form.save()
            vendor = vendorform.save(commit=False)
            vendor.vendoruser = user
            get_vendor_username =form.cleaned_data['username']
            print(get_vendor_username)
            vendor.vendor_slug = slugify(get_vendor_username)
            userprofile = UserProfileModel.objects.get(user = user)
            vendor.vendor_profile = userprofile
            vendor.save()
            #send email verification 
            send_verification_email(request , user)
            messages.success(request , 'Your account has been registered sucessfully ! , please wait for approval')
            return redirect('registervendor')

        else :
            print(form.errors , vendorform.errors)
            context={
                'form' : form ,
                'vendorform' : vendorform

            }
            return render(request , 'accounts/registervendor.html' , context)

def activate(request , uidb64 , token):
    #activated with is_active to True 
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk = uid)
    
    except(ValueError , TypeError , OverflowError , UserModel.DoesNotExist) :
        user = None
        
    if user is not None and default_token_generator.check_token(user , token):
        user.is_active = True
        user.save()
        messages.success(request , "your email address and account have been confirmed !")
        return redirect('myaccount')

    else :
        messages.error(request , 'invalid link or token ! try again .')
        return redirect("myaccount")


class LoginView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request , "you are already logged in !")
            return redirect("myaccount")
        return render(request , "accounts/login.html")
    
    def post(self , request):
        email = request.POST['email']
        password = request.POST['password']
        
        authentication = auth.authenticate(email=email , password = password)
        
        if authentication is not None :
            auth.login(request , authentication)
            messages.success(request,"you login successfully !")
            return redirect('myaccount')
        
        else :
            messages.error(request , "Invalid informations !")
            return redirect('login')

def logout(request):
    auth.logout(request)
    messages.info( request,'you are logged out !')
    return redirect('login')            

@login_required(login_url='login')
def MyAccount(request):
    user = request.user
    redirecturl = DetectUser(user)
    return redirect(redirecturl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def CDashBoard(request):
    orders = OrderModel.objects.filter(user = request.user , is_ordered = True)
    recent_orders = OrderModel.objects.filter(user = request.user , is_ordered = True).order_by('-created_at')[:5]
    context = {
        'orders' : orders,
        'recent_orders' : recent_orders ,
        'orders_count' : orders.count()
    }
    return render(request , 'accounts/cdashboard.html' , context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def VDashBoard(request):
    vendor = VendorModel.objects.get(vendoruser = request.user)
    context = {
        'vendor':vendor
    }
    return render(request , 'accounts/vdashboard.html', context)

class forgot_password(View):
    def get(self , request):
        return render(request , 'accounts/forgot_password.html')
    
    def post(self , request):
        email = request.POST['email']

        if UserModel.objects.filter(email = email).exists():
            user = UserModel.objects.get(email__exact = email)

            #send reset email 
            send_reset_password_email(request , user)

            messages.success(request , "Reset Password Link send to your email !")
            return redirect('login')
        else :
            messages.warning(request , "Your Email It doesn't exist yet ")
            return redirect("forgot_password")

def reset_password_validate(request , uidb64 , token):
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk = uid)
    
    except(ValueError , TypeError , OverflowError , UserModel.DoesNotExist) :
        user = None
        
    if user is not None and default_token_generator.check_token(user , token):
        request.session['uid'] = uid 
        messages.info(request , 'please reset your password')
        return redirect('reset_password')
    else :
        messages.error(request , 'This link has been expired !')
        return redirect('login')


class reset_password(View):

    def get(self , request):
        return render(request , 'accounts/reset_password.html')
    
    def post(self , request):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password :
            uid = request.session.get('uid')
            user = UserModel.objects.get(pk = uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request , "The password was changed !")
            return redirect('login')
        else :
            messages.error(request , 'password do not match')
            return redirect('reset_password')

