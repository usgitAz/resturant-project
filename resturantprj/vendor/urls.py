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


]
