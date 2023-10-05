from django.shortcuts import render , redirect
from django.contrib import messages
from vendor.models import OpeningHourModel, VendorModel
from django.shortcuts import get_object_or_404
from menu.models import CategoryModel , FooditemModel
from django.db.models import Prefetch
from django.http import HttpResponse , JsonResponse
from .models import CartModel
from .context_processors import get_cart_counter , get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from datetime import date, datetime
from orders.forms import OrderForm
from accounts.models import UserProfileModel

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
    ) # to acsess to food item in food item model beacuse we have forigen key categort in food item  we use prefetch related

    opening_hours = OpeningHourModel.objects.filter(vendor = vendor).order_by('day' , '-from_hour')
    # check current day  to show opening hour 
    today = date.today().isoweekday()
    
    current_day = OpeningHourModel.objects.filter(vendor = vendor , day = today)

    if request.user.is_authenticated:
         cart_items = CartModel.objects.filter(user = request.user)
    else :
         cart_items = None
    context = {
        'vendor' : vendor,
        "categories" : categories,
        "cart_items" : cart_items,
        'opening_hours' : opening_hours,
        'current_day' : current_day,
    }
    return render(request , 'marketplace/vendor_detail.html', context)

def add_to_cart(request , food_id):
    if request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                #check food item exist 
                try:
                    fooditem = FooditemModel.objects.get(id = food_id)
                    #check the user has already add that food to the card
                    try :
                         check_cart = CartModel.objects.get(user=request.user , fooditem = fooditem)
                         #increase the cart quantity
                         check_cart.quantity += 1
                         check_cart.save()
                         return JsonResponse({'status':'success' , 'message' : "increase the cart quantiy" , 'cart_counter' : get_cart_counter(request), 'qty' : check_cart.quantity , 'cart_amount' : get_cart_amounts(request)  })
                         
                    except:
                        check_cart = CartModel.objects.create(user = request.user , fooditem=fooditem , quantity=1)
                        return JsonResponse({'status':'success' , 'message' : "Added food the Cart" , 'cart_counter' : get_cart_counter(request) , 'qty' : check_cart.quantity  , 'cart_amount' : get_cart_amounts(request) })

                         
                except:
                    return JsonResponse({'status':'failed' , 'message' : "This food is not exist !"})
            else:
                 return JsonResponse({'status':'failed' , 'message' : "Invalid Request !"})
            
    else:
        return JsonResponse({'status':'login_required' , 'message' : "Please Login to Continue"})
    

def decrease_cart(request , food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check food item exist 
            try:
                fooditem = FooditemModel.objects.get(id = food_id)
                #check the user has already add that food to the card
                try :
                    check_cart = CartModel.objects.get(user=request.user , fooditem = fooditem)
                    if check_cart.quantity > 1 :
                        #decrease the cart quantity
                        check_cart.quantity -= 1
                        check_cart.save()
                    else :
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({'status':'success' , 'message' : "Decrease the cart quantiy" , 'cart_counter' : get_cart_counter(request), 'qty' : check_cart.quantity , 'cart_amount' : get_cart_amounts(request)   })
                        
                except:
                    return JsonResponse({'status':'failed' , 'message' : "You dont have this item in your cart" })

                        
            except:
                return JsonResponse({'status':'failed' , 'message' : "This food is not exist !"})
        else:
                return JsonResponse({'status':'failed' , 'message' : "Invalid Request !"})
            
    else:
        return JsonResponse({'status':'login_required' , 'message' : "Please Login to Continue"})
    


@login_required(login_url='login')
def cart(request):
    cart_items = CartModel.objects.filter(user=request.user).order_by('-updated_at') #show last change on top of cart page by order
    context = {
        'cart_items' : cart_items ,
    }
    return render(request , 'marketplace/cart.html' , context)


def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = CartModel.objects.get(user=request.user , id=cart_id)
                if cart_item :
                    cart_item.delete()
                    return JsonResponse({'status':'success' , 'message' : "Cart deleted sucessfully" , 'cart_counter' : get_cart_counter(request) , 'cart_amount' : get_cart_amounts(request)  })
            except:
                return JsonResponse({'status':'failed' , 'message' : "Cart item does not exist!" })
        else :
            return JsonResponse({'status':'failed' , 'message' : "Invalid Request !"})
    else :
        return JsonResponse({'status':'login_required' , 'message' : "Please Login to Continue"})
    


def search(request):
    if not 'address' in request.GET :
        return redirect("marketplace")
    try :
        keyword = request.GET['keyword']
        address = request.GET['address']
        latitude = request.GET['lat']
        longtitude = request.GET['long']
        radius = request.GET['radius']
    except :
        messages.error(request , "invalid request , please check youe entered informations !!")
        return redirect('mainpage')

    fetch_vendors_by_fooditems = FooditemModel.objects.filter(food_title__icontains= keyword ,is_available = True  ).values_list('vendor' , flat= True)

    vendors= VendorModel.objects.filter(Q(id__in = fetch_vendors_by_fooditems) | Q(vendor_name__icontains = keyword , is_approved = True , vendoruser__is_active = True))
    if latitude and longtitude and radius :
        pnt = GEOSGeometry(f"POINT({longtitude} {latitude})", srid=4326)

        vendors= VendorModel.objects.filter(Q(id__in = fetch_vendors_by_fooditems) | Q(vendor_name__icontains = keyword , is_approved = True , vendoruser__is_active = True)
         , vendor_profile__location__distance_lte=(pnt, D(km=radius))).annotate (distance = Distance("vendor_profile__location" , pnt)).order_by("distance")

        for v in vendors :
            v.kms = round(v.distance.km , 1)

    count_vendors = vendors.count()
    context = {
        'vendors' : vendors ,
        'count_vendors' : count_vendors,
        'source_location' : address,
    }
    
    return render(request , 'marketplace/listings.html' , context)

@login_required(login_url='login')
def checkout(request):
    cart_items = CartModel.objects.filter(user = request.user  ).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0 :       
        messages.info(request , "you dont have any selected product first add somting food !")
        return redirect('marketplace')
    profile_model = UserProfileModel.objects.get(user=request.user)
    values ={
        'first_name' : request.user.first_name,
        'last_name' : request.user.last_name,
        'email' : request.user.email,
        'address' : profile_model.address,
        'country' : profile_model.country,
        'state' : profile_model.state,
        'city' : profile_model.city,
        

    }
    order_form = OrderForm(initial=values)
    context = {
        'order_form' : order_form , 
        'cart_items' : cart_items,
    }
    return render(request , "marketplace/checkout.html" , context)