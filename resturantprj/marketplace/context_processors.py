from .models import CartModel , Taxmodel
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
    toman = 0
    subtotal = 0 
    tax = 0
    total = 0
    tax_dict = {}
    if request.user.is_authenticated :
        cart_items = CartModel.objects.filter(user= request.user)
        for item in cart_items :
            food_item = FooditemModel.objects.get(pk = item.fooditem.id)
            subtotal += (food_item.price *item.quantity)
       
        #calc price tax
        get_tax = Taxmodel.objects.filter(is_active= True)
        for i in get_tax :
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((i.tax_percentage * subtotal)/100 , 2) #get tax amount by total price * tax precent /100 
            tax_dict.update({tax_type : {str(tax_percentage) : tax_amount}})

        # clac all tax in modeltax
        tax = 0
        for key in tax_dict.values():
            for x in key.values():
                tax = tax + x
        
    
        total = subtotal + tax
        toman = int( total * 50000)
    return dict(subtotal = subtotal , tax = tax , total = total , tax_dict = tax_dict , toman=toman)

