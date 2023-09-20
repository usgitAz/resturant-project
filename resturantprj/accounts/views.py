from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views import View
from .forms import UserForm
from .models import UserModel
from django.contrib import messages
# Create your views here.


class RegisterUserView(View):
    form = UserForm()
    context={
        'form' : form
    }
    def get(self ,request):
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
        