from django.urls import path
from accounts import views as accountviews
from . import views
urlpatterns = [
    path("" , accountviews.CDashBoard , name="CDashBoard" ),
    path("profile/" , views.CProfile , name = "cprofile"),
]
