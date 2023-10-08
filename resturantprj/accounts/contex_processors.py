from django.conf import settings
from vendor.models import VendorModel

def get_vendor(request):
    try :
        vendor = VendorModel.objects.get(vendoruser = request.user)
    except:
        vendor = None
    return dict(vendor=vendor)



def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID' : settings.PAYPAL_CLIENT_ID}