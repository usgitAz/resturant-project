from django.http import HttpResponse , JsonResponse
from django.shortcuts import render , redirect
from django.contrib import messages
from marketplace.models import CartModel
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import OrderModel, OrderedFoodModel, PaymentModel
import simplejson as json
from .utils import generate_order_number
from django.views.decorators.csrf import csrf_protect
from accounts.Utils import send_notification_email
from django.contrib.auth.decorators import login_required
# Create your views here.



@login_required(login_url="login")
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

@login_required(login_url="login")
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

        #move the cart items to order food model 
        cart_items = CartModel.objects.filter(user = request.user)
        for item in cart_items :
            orderred_food = OrderedFoodModel()
            orderred_food.order = order
            orderred_food.payment = payment
            orderred_food.user = request.user
            orderred_food.fooditem = item.fooditem
            orderred_food.quantity = item.quantity
            orderred_food.price = item.fooditem.price
            orderred_food.amount = item.fooditem.price * item.quantity # total amount
            orderred_food.save()
            
        


        #send order recived email to customer 
        mail_subject = 'Thanks for ordering with us .'
        mail_template =  'orders/emails/order_email_confirmation.html'
        context = {
            'user' : request.user , 
            'order' : order,
            'to_email' : order.email,
        }
        send_notification_email(mail_subject , mail_template , context)

        #send order recived email to vendors
        mail_subject = "You have recived a new order ."
        mail_template = "orders/emails/recived_order_to_vendor.html"
        to_eamils = []
        for i in cart_items :
            if i.fooditem.vendor.vendoruser.email not in to_eamils: #just 1 uniq address we need in list 
                to_eamils.append(i.fooditem.vendor.vendoruser.email)
        print(to_eamils)
        context={
            'order' : order ,
            'to_email' : to_eamils ,
        }

        send_notification_email(mail_subject , mail_template , context)


        #clear the cart if the payment is sucess 
        cart_items.delete()
        response = {
            'order_number' : order_number ,
            'transaction_id' : transaction_id,
        }
        return JsonResponse(response)
        #retirn back to ajax with status success or faild

    return HttpResponse('payment view ')


def order_complate(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get('transaction_id')
    try :
        order = OrderModel.objects.get(order_number=order_number , payment__transaction_id = transaction_id , is_ordered=True )
        ordered_food = OrderedFoodModel.objects.filter(order = order)

        subtotal = 0
        for item in ordered_food :
            subtotal += (item.price * item.quantity)

        tax_data = json.loads(order.tax_data)
        print(tax_data)
        context ={
            'order' : order,
            'ordered_food' : ordered_food,
            'subtotal' : subtotal,
            'tax_data' : tax_data,
        }
        return render (request , 'orders/order_complate.html' , context)
    except:
        return redirect('mainpage')
    return render(request , "orders/order_complate.html")