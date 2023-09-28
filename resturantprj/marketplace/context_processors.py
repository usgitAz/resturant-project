from .models import CartModel
from menu.models import FooditemModel

def get_cart_counter(request):
    cart_count= 0
    if request.user.is_authenticated :
        try:
            cart_items = CartModel.objects.filter(user = request.user)
            if cart_items :
                for cart_item in cart_items :
                    cart_count += cart_item.quantity
            else :
                cart_count = 0
        except :
            cart_count = 0
    return dict(cart_count = cart_count)



def get_cart_amounts(request):
    subtotal = 0 
    tax = 0
    total = 0
    if request.user.is_authenticated :
        cart_items = CartModel.objects.filter(user= request.user)
        for item in cart_items :
            food_item = FooditemModel.objects.get(pk = item.fooditem.id)
            subtotal += (food_item.price *item.quantity)
        total = subtotal + tax
    return dict(subtotal = subtotal , tax = tax , total = total)

