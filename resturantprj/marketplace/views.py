from django.shortcuts import render
from vendor.models import VendorModel
from django.shortcuts import get_object_or_404
from menu.models import CategoryModel , FooditemModel
from django.db.models import Prefetch
from django.http import HttpResponse , JsonResponse
from .models import CartModel
from .context_processors import get_cart_counter , get_cart_amounts
from django.contrib.auth.decorators import login_required
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
    if request.user.is_authenticated:
         cart_items = CartModel.objects.filter(user = request.user)
    else :
         cart_items = None
    context = {
        'vendor' : vendor,
        "categories" : categories,
        "cart_items" : cart_items,
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