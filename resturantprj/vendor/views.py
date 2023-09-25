from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from .forms import VendorForm
from accounts.forms import UserProfileForm
from .models import VendorModel
from accounts.models import UserProfileModel 
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from accounts.views import check_role_vendor
from menu.models import CategoryModel , FooditemModel
from menu.form import CategoryForm
from django.template.defaultfilters import slugify
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
    fooditems = FooditemModel.objects.filter(vendor=vendor , category=category)
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