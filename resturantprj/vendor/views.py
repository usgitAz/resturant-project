from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from .forms import VendorForm
from accounts.forms import UserProfileForm
from .models import VendorModel
from accounts.models import UserProfileModel
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from accounts.views import check_role_vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorprofileview(request):

    profile = get_object_or_404(UserProfileModel , user = request.user)
    vendor = get_object_or_404(VendorModel , vendoruser = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST , request.FILES , instance=profile)
        vendor_form = VendorForm(request.POST , request.FILES , instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request , "your changes are saved !")
            return redirect('VDashBoard')
        else :
            messages.error(request , "Invalid information !! check entered files and inputs and try again .")
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)  

    context ={
        'profile_form' : profile_form ,
        'vendor_form' : vendor_form,
        'profile': profile ,
        'vendor' : vendor ,
    }
    
    return render(request , 'vendor/vendor-profile.html' , context)


