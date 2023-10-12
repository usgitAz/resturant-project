from django.db import IntegrityError
from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from orders.models import OrderModel, OrderedFoodModel
from .forms import VendorForm , OpeningHourForm
from accounts.forms import UserProfileForm 
from .models import VendorModel , OpeningHourModel
from accounts.models import UserProfileModel 
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test 
from accounts.views import check_role_vendor
from menu.models import CategoryModel , FooditemModel
from menu.form import CategoryForm , FoodItemForm
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate , login
from django.utils.decorators import method_decorator


def get_vendor(request):
    return VendorModel.objects.get(vendoruser =request.user)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorprofileview(request):

    profile = get_object_or_404(UserProfileModel , user = request.user)
    vendor = get_object_or_404(VendorModel , vendoruser = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST , request.FILES , instance=profile)
        vendor_form = VendorForm(request.POST , request.FILES , instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request , "your changes are saved !")
            return redirect('VDashBoard')
        else :
            messages.error(request , "Invalid information !! check entered files and inputs and try again .")
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)  

    context ={
        'profile_form' : profile_form ,
        'vendor_form' : vendor_form,
        'profile': profile ,
        'vendor' : vendor ,
    }
    
    return render(request , 'vendor/vendor-profile.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = VendorModel.objects.get(vendoruser=request.user)
    categories =  CategoryModel.objects.filter(vendor = vendor).order_by('created_at')
    context = {
        'categories' : categories
    }
    return render(request , 'vendor/menu_builder.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request , pk=None):
    vendor = VendorModel.objects.get(vendoruser=request.user)
    category =  get_object_or_404(CategoryModel , pk=pk)
    fooditems = FooditemModel.objects.filter(vendor=vendor , category=category).order_by('created_at')
    context = {
        'category' : category,
        'fooditems' : fooditems,
    }
    return render(request , 'vendor/fooditems_by_category.html' , context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor =  vendor = VendorModel.objects.get(vendoruser=request.user)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request , ' New Category Added now !')
            return redirect("menu_builder")
        else :
            messages.warning(request,'error ! check the entered informations and try again !')
            context ={
                'form' : form
            }
            return render(request , 'vendor/add_category.html' , context)
            print(form.errors)
    form = CategoryForm()
    context ={
        'form' : form
    }
    return render(request , 'vendor/add_category.html' , context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category (request , pk):
    category =  get_object_or_404(CategoryModel , pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST , instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor =  vendor = VendorModel.objects.get(vendoruser=request.user)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request , 'Category updated ')
            return redirect("menu_builder")
        else :
            messages.warning(request,'error ! check the entered informations and try again !')
            context ={
                'form' : form
            }
            return render(request , 'vendor/add_category.html' , context)
            print(form.errors)
    form = CategoryForm(instance=category)
    context ={
        'form' : form,
        'category' : category
    }
    return render(request , 'vendor/edit_category.html', context )

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request , pk):
    category =  get_object_or_404(CategoryModel , pk=pk)
    category.delete()
    messages.info(request , 'Category removed')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST , request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor =  vendor = VendorModel.objects.get(vendoruser=request.user)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request , ' New Food Added now !')
            return redirect("fooditems_by_category" , food.category.id)
        else :
            messages.warning(request,'error ! check the entered informations and try again !')
            context ={
                'form' : form
            }
            return render(request , 'vendor/add_category.html' , context)
            print(form.errors)
    else:
        form = FoodItemForm()
        #modify this form to show only query to vendor queries
        form.fields['category'].queryset = CategoryModel.objects.filter(vendor = VendorModel.objects.get(vendoruser = request.user))
         
    centext ={
        'form':form
    }
    return render(request , "vendor/add_food.html" , centext)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request , pk):
    fooditems =  get_object_or_404(FooditemModel , pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST ,request.FILES, instance=fooditems)
        if form.is_valid():
            food_name = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor =  vendor = VendorModel.objects.get(vendoruser=request.user)
            food.slug = slugify(food_name)
            form.save()
            messages.success(request , 'Food updated ')
            return redirect("fooditems_by_category" , food.category.id)
        else :
            messages.warning(request,'error ! check the entered informations and try again !')
            # context ={
            #     'form' : form
            # }
            # return render(request , 'vendor/add_category.html' , context)
            print(form.errors)
    else :
        form = FoodItemForm(instance=fooditems)
        form.fields['category'].queryset = CategoryModel.objects.filter(vendor = VendorModel.objects.get(vendoruser = request.user))
        
    context ={
        'form' : form,
        'food' : fooditems
    }
    return render(request , 'vendor/edit_food.html' , context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request , pk):
    food =  get_object_or_404(FooditemModel , pk=pk)
    food.delete()
    messages.info(request , 'Fooditem removed')
    return redirect("fooditems_by_category" , food.category.id)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def opening_hours(request):
    opening_hours = OpeningHourModel.objects.filter(vendor__vendoruser = request.user)
    form = OpeningHourForm()
    context = {
        'form' : form ,
        'opening_hours' : opening_hours,
    }
    return render(request , 'vendor/opening_hours.html' , context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def opening_hours_add(request):
    # handle data and save to db
    if request.user.is_authenticated:
        
        if request.headers.get("x-requested-with") == "XMLHttpRequest" and request.method == "POST":
            day = request.POST.get("day")
            from_hour = request.POST.get("from_hour")
            to_hour = request.POST.get("to_hour")
            is_closed = request.POST.get("is_closed")
            print(day, from_hour, to_hour, is_closed)
            try:
                if hour := OpeningHourModel.objects.create(
                    vendor=get_vendor(request),
                    day=day,
                    from_hour=from_hour,
                    to_hour=to_hour,
                    is_closed=is_closed,
                ):
                    day = OpeningHourModel.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status': 'success', 'id': hour.id, 'day':day.get_day_display(), 'is_closed':'Closed'}
                    else:
                        response = {'status': 'success', 'id': hour.id, 'day':day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}

                return JsonResponse(response)

            except IntegrityError:
                response = {'status': 'failed', 'message':from_hour +'-'+to_hour + ' already exist for this day.'}
                return JsonResponse(response)

    else:
        HttpResponse("Invalid Request") 

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def opening_hours_remove(request , pk):
     if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            hour = get_object_or_404(OpeningHourModel , pk=pk)
            hour.delete()
            return JsonResponse({'status' : 'success' , 'id' : pk})


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def order_detail(request , order_number):
    try:
        order = OrderModel.objects.get(order_number = order_number , is_ordered = True)
        ordered_food = OrderedFoodModel.objects.filter(order = order , fooditem__vendor = get_vendor(request))
        context = {
            'order':order , 
            'ordered_food' : ordered_food ,
            'subtotal' : order.get_total_by_vendor()['subtotal'],
            'tax_data' : order.get_total_by_vendor()['tax_dict'],
            'total' : order.get_total_by_vendor()['total'],
        }
    except :
        messages.error(request, 'eror detail order not found !')
        return redirect('vendor')
    return render(request , 'vendor/order_detail.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def orders(request):
    vendor = VendorModel.objects.get(vendoruser = request.user)
    orders = OrderModel.objects.filter(vendors__in =[vendor.id], is_ordered=True).order_by('-created_at')
    context={
        'orders' : orders
    }
    return render(request , 'vendor/orders.html' , context)


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(user_passes_test(check_role_vendor) , name='dispatch')
class change_password(View):
    def get(self , request):
        return render(request , "vendor/change_password.html")
    
    def post(self , request):
        old_password = request.POST['current_password']
        new_password = request.POST['new_password']
        verify_password = request.POST['verify_password']
        
        user = authenticate(email=request.user.email , password = old_password)
        
        if user is not None:
            if new_password == verify_password:
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request , "your password changed successfully!")
                return redirect('VDashBoard')
            else:
                messages.error(request , "New Password not match ! try again .")
                return render(request, 'vendor/change_password.html')
        else:
            messages.error(request , 'Invalid Old Password try again !')
            return render(request, 'vendor/change_password.html')