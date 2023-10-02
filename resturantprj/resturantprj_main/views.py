from django.shortcuts import render
from vendor.models import VendorModel
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance


def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng , lat
    elif 'lat' in request.GET :
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng , lat
    else :
        return None

def mainpage(request):
    if get_or_set_current_location(request) is not None :
        pnt = GEOSGeometry("POINT(%s %s)" %(get_or_set_current_location(request)))

        vendors= VendorModel.objects.filter(vendor_profile__location__distance_lte=(pnt, D(km=1000))).annotate (distance = Distance("vendor_profile__location" , pnt)).order_by("distance")

        for v in vendors :
            v.kms = round(v.distance.km , 1)
    else :
        vendors = VendorModel.objects.filter(is_approved = True , vendoruser__is_active = True)[:8]
    context ={
        'vendors' : vendors
    }
    return render(request , "mainpage.html", context)