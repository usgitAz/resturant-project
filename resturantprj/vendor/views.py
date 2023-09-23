from django.shortcuts import render
# Create your views here.


def vendorprofile(request):
    return render(request , 'vendor/vendor-profile.html')