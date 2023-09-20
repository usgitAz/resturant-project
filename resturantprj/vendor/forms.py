from django import forms
from .models import VendorModel

class VendorForm(forms.ModelForm):
    class Meta:
        model = VendorModel
        fields = ['vendor_name' ,'vendor_license']
        error_messages = {
            "vendor_name" :{
                "required" : "Please Enter your resturant name  !"
            },
            "vendor_license" :{
                "required" : "Please Enter your resturant licence  !"
            },
        }
