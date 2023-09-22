from django.contrib import admin
from .models import VendorModel
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ("vendoruser" , "vendor_name" , "is_approved" ,"created_at")
    ordering = ("-created_at" , )
    list_editable = ('is_approved' ,)

admin.site.register(VendorModel , VendorAdmin)