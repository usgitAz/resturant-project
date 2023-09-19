from django.urls import path
from . import views


urlpatterns = [
    path('registeruser/' , views.RegisterUserView.as_view(), name='registeruser')
]
