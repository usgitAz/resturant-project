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
    path('activate/<uidb64>/<token>/' , views.activate , name='activate'),
    path('forgot_password/' , views.forgot_password.as_view() , name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/' , views.reset_password_validate , name='reset_password_validate',),
    path('reset_password' , views.reset_password.as_view() , name='reset_password') 
    
]
