from django.urls import path
from .import views
urlpatterns = [
    path('placeorder/' , views.place_order , name='place_order'),
]

