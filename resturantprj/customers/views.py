from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm , UserInforForm
from accounts.models import UserProfileModel
from django.contrib import messages

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