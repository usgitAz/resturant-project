from django.conf import settings
from accounts.models import UserProfileModel
from vendor.models import VendorModel

def get_vendor(request):
    try :
        vendor = VendorModel.objects.get(vendoruser = request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_user_profile(request):
    try:
        user_profile = UserProfileModel.objects.get(user = request.user)
    except :
        user_profile = None
    return dict(user_profile = user_profile)

def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID' : settings.PAYPAL_CLIENT_ID}