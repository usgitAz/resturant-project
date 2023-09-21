from django.urls import path
from . import views


urlpatterns = [
    path('registeruser/' , views.RegisterUserView.as_view(), name='registeruser'),
    path('registervendor/' , views.RegisterVendorView.as_view(), name='registervendor'),
    path('login/' , views.LoginView.as_view() , name='login'),
    path('logout/' , views.logout , name='logout'),
    path('myaccount/' , views.MyAccount , name='myaccount'),
    path('CDashBoard/', views.CDashBoard , name="CDashBoard"),
    path('VDashBoard/' , views.VDashBoard , name='VDashBoard'),
 
]
