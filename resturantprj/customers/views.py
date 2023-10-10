from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from accounts.forms import UserProfileForm , UserInforForm
from accounts.models import UserProfileModel
from django.contrib import messages

from orders.models import OrderModel, OrderedFoodModel
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

@login_required(login_url='login')
def CProfile(request):
    profile = get_object_or_404(UserProfileModel , user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm( request.POST, request.FILES,instance=profile)
        user_form = UserInforForm( request.POST , instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request , "Your information are updated!")
            return redirect('cprofile')
        else:
            messages.error(request , "Invalid inforamations ! check the erors field and try again .")
            return redirect('cprofile')

    else:

        profile_form = UserProfileForm(instance=profile)
        user_form = UserInforForm(instance=request.user)

    context = {
        'profile_form' : profile_form ,
        'user_form' : user_form,
        'profile' : profile
    }
    return render(request, "customers/customerprofile.html" , context)

@login_required(login_url='login')
def my_orders(request):
    orders = OrderModel.objects.filter(user = request.user , is_ordered = True).order_by('-created_at')
    context = {
        'orders' : orders,
    }
    return render(request , 'customers/my_orders.html' , context)

@login_required(login_url='login')
def order_detail(request , order_number):
    try :
        order = OrderModel.objects.get(order_number = order_number , is_ordered = True)
        ordered_food = OrderedFoodModel.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food :
            subtotal += (item.price * item.quantity)
        tax_data  = json.loads(order.tax_data)
        context = {
            'order' : order,
            'ordered_food' : ordered_food,
            'subtotal' : subtotal,
            'tax_data' : tax_data
        }
        return render(request , "customers/order_detail.html" , context)
    except:
        messages.error(request , 'invalid order number !')
        return redirect('CDashBoard')


class change_password(View):

    def get(self , request):
        return render(request , "customers/change_password.html")
    
    def post(self , request):
        old_password = request.POST['current_password']
        new_password = request.POST['new_password']
        verify_password = request.POST['verify_password']
        
        user = authenticate(email=request.user.email , password = old_password)
        
        if user is not None:
            if new_password == verify_password:
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request , "your password changed successfully!")
                return redirect('CDashBoard')
            else:
                messages.error(request , "New Password not match ! try again .")
                return render(request, 'customers/change_password.html')
        else:
            messages.error(request , 'Invalid Old Password try again !')
            return render(request, 'customers/change_password.html')
    
    