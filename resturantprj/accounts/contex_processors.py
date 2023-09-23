from vendor.models import VendorModel

def get_vendor(request):
    try :
        vendor = VendorModel.objects.get(vendoruser = request.user)
    except:
        vendor = None
    return dict(vendor=vendor)