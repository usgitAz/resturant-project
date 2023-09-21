from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views import View
from .forms import UserForm
from .models import UserModel , UserProfileModel
from vendor.forms import VendorForm
from django.contrib import messages , auth
from .Utils import DetectUser , check_role_customer , check_role_vendor
from django.contrib.auth.decorators import login_required , user_passes_test
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
            messages.success(request , 'Your account has been registered sucessfully !')
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
            user.role= UserModel.RESTURANT
            form.save()
            vendor = vendorform.save(commit=False)
            vendor.vendoruser = user
            userprofile = UserProfileModel.objects.get(user = user)
            vendor.vendor_profile = userprofile
            vendor.save()
            messages.success(request , 'Your account has been registered sucessfully ! , please wait for approval')
            return redirect('registervendor')

        else :
            print(form.errors , vendorform.errors)
            context={
                'form' : form ,
                'vendorform' : vendorform

            }
            return render(request , 'accounts/registervendor.html' , context)


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
    return render(request , 'accounts/cdashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def VDashBoard(request):
    return render(request , 'accounts/vdashboard.html')
