from django.urls import path
from .import views
urlpatterns = [
    path('placeorder/' , views.place_order , name='place_order'),
    path('payments/' , views.payments , name='payments'),
    path('order_complate' , views.order_complate , name='order_complate'),
]

