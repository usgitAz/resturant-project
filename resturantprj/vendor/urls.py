from django.urls import path
from . import views
from accounts import views as accountviews

urlpatterns = [
    path('' , accountviews.MyAccount , name = 'vendor' ),
    path('profile/' , views.vendorprofileview, name='vendorprofile'),
    path('menu-builder' , views.menu_builder , name='menu_builder'),
    path('menu-builder/category/<int:pk>' , views.fooditems_by_category , name='fooditems_by_category'),
    path('menu-builder/category/add' , views.add_category , name='add_category'),
    path('menu-builder/category/edit/<int:pk>' , views.edit_category , name='edit_category'),
    path('menu-builder/category/delete/<int:pk>' , views.delete_category , name='delete_category'),
    path('menu-builder/food/add/' , views.add_food , name='add_food'),
    path('menu-builder/food/edit/<int:pk>/' , views.edit_food , name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/' , views.delete_food , name='delete_food'),
    path('opening_hours/' , views.opening_hours , name='opening_hours'),
    path('opening_hours/add/' , views.opening_hours_add , name='opening_hours_add'),
    path('opening_hours/remove/<int:pk>/' , views.opening_hours_remove , name='opening_hours_remove'),
    path('order_detail/<int:order_number>/', views.order_detail , name='vendor_order_detail'),
    path('orders' , views.orders , name='vendor_orders' ),
    path('change_password/', views.change_password.as_view() , name='vendor_change_password')
     

]
