from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib import messages
from marketplace.models import CartModel
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import OrderModel, PaymentModel
import simplejson as json
from .utils import generate_order_number
from django.views.decorators.csrf import csrf_protect
# Create your views here.

@csrf_protect
#use csrf to save data in to database
def place_order(request):  
    cart_items = CartModel.objects.filter(user = request.user  ).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0 :       
        messages.info(request , "you dont have any selected product first add somting food !")
        return redirect('marketplace')
    
    subtotal = get_cart_amounts(request)['subtotal']
    tax = get_cart_amounts(request)['tax']
    total = get_cart_amounts(request)['total']
    tax_data = get_cart_amounts(request)['tax_dict']

    if request.method == 'POST':
        form = OrderForm(request.POST)    
        if form.is_valid():
            order = OrderModel()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.user = request.user
            order.total = total
            order.total_tax = tax
            order.tax_data = json.dumps(tax_data)
            order.payment_method = request.POST['pyment-method']
            order.order_number = generate_order_number(request.user.pk)
            order.save()
            context = {
                'order': order ,
                'cart_items' : cart_items ,
            }
            return render (request , "orders/place_order.html" , context)
   
    else :
        print(form.errors)
    
    return render(request , "orders/place_order.html")


def payments(request):
    #check if request is ajax
    if request.method == 'POST' or request.headers.get("x-requested-with") == "XMLHttpRrequest":
        #get data from request
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        csrf = request.POST.get('csrfmiddlewaretoken')
        #store the payment details in the payment model 
        order = OrderModel.objects.get(user = request.user  , order_number = order_number)        
        payment = PaymentModel.objects.create(
            user = order.user ,
            transaction_id = transaction_id ,
            payment_method = payment_method ,
            amount = order.total ,
            status = status,
        )

        #update the order model 
        order.payment = payment
        order.is_ordered = True
        order.save()
        return HttpResponse("order Updated !")
        #move the cart items to order food model 

        #send order recived ematil to vendor 

        #clear the cart if the payment is sucess 

        #retirn back to ajax with status success or faild

    return HttpResponse('payment view ')
