from django.shortcuts import render
from vendor.models import VendorModel
from django.shortcuts import get_object_or_404
from menu.models import CategoryModel , FooditemModel
from django.db.models import Prefetch
# Create your views here.

def marketplace(request):
    vendors = VendorModel.objects.filter(is_approved = True , vendoruser__is_active = True)
    #count vendors
    count_vendors = vendors.count()
    context ={
        'vendors' : vendors ,
        'count_vendors' : count_vendors
    }
    return render(request , 'marketplace/listings.html' , context)


def vendor_detail(request , vendor_slug):
    vendor = get_object_or_404(VendorModel , vendor_slug=vendor_slug)
    categories = CategoryModel.objects.filter(vendor = vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FooditemModel.objects.filter(is_available =True),
        )
    ) # to acsess to food item in food item model beacuse we have forigen key categort in food item  we user prefetch related
    context = {
        'vendor' : vendor,
        "categories" : categories,
    }
    return render(request , 'marketplace/vendor_detail.html', context)