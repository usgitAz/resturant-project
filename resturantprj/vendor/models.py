from django.db import models
from accounts.models import UserModel , UserProfileModel
# Create your models here.


class VendorModel(models.Model):
    vendoruser= models.OneToOneField(UserModel , related_name='UserModel'  , on_delete=models.CASCADE )
    vendor_profile = models.OneToOneField(UserProfileModel , related_name='UserProfileModel' , on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.FileField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.vendor_name}"
    