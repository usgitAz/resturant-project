from django.shortcuts import render
from vendor.models import VendorModel

def mainpage(request):
    vendors = VendorModel.objects.filter(is_approved = True , vendoruser__is_active = True)[:8]
    context ={
        'vendors' : vendors
    }
    return render(request , "mainpage.html", context)