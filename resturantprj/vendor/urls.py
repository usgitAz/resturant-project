from django.urls import path
from . import views
from accounts import views as accountviews

urlpatterns = [
    path('' , accountviews.MyAccount , name = 'vendor' ),
    path('profile/' , views.vendorprofileview, name='vendorprofile'),
]
