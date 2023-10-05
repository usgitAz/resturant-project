from django.shortcuts import render , redirect
from django.contrib import messages
from marketplace.models import CartModel
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import OrderModel
import simplejson as json
from .utils import generate_order_number
# Create your views here.

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
        else :
            print(form.errors)
    else :
        print(request.method)
    
    return render(request , "orders/place_order.html")