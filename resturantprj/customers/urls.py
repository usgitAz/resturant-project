from django.urls import path
from accounts import views as accountviews
from . import views
urlpatterns = [
    path("" , accountviews.CDashBoard , name="CDashBoard" ),
    path("profile/" , views.CProfile , name = "cprofile"),
    path('my_orders/', views.my_orders , name='my_orders'),
    path('order_detail/<int:order_number>' , views.order_detail , name='order_detail'),
    path('change_password/' , views.change_password.as_view(), name='change_password'),
]
