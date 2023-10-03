from django.contrib import admin
from .models import VendorModel , OpeningHourModel
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ("vendoruser" , "vendor_name" , "is_approved" ,"created_at")
    ordering = ("-created_at" , )
    list_editable = ('is_approved' ,)

class OpeningHourAdmin(admin.ModelAdmin):
     list_display = ('vendor' , 'day' , 'from_hour', 'to_hour')

admin.site.register(VendorModel , VendorAdmin)
admin.site.register(OpeningHourModel ,OpeningHourAdmin )