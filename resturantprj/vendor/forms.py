from django import forms
from .models import VendorModel
from accounts.validators import allow_only_images_validator
class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn.btn-info'}) , validators=[allow_only_images_validator])

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
