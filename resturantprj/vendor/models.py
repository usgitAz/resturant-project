from django.db import models
from accounts.models import UserModel , UserProfileModel
from accounts.Utils import send_notification_email
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
    
    def save(self , *args, **kwargs):
        if self.pk is not None:
            account = VendorModel.objects.get(pk=self.pk)
            if account.is_approved != self.is_approved :
                mail_template = 'accounts/emails/admin_approval_email.html'

                context = {
                        'user' : self.vendoruser ,
                        'is_approved' : self.is_approved,
                    }
                if self.is_approved == True :
                    #send email to user
                    mail_subject = 'Your resturant approved by admin !'
                    send_notification_email(mail_subject ,mail_template , context)
                else:
                    #send email to user
                    mail_subject = 'Attention! Your account has been suspended by the admin'
                    send_notification_email(mail_subject ,mail_template , context)

        return super(VendorModel , self).save(*args, **kwargs)
    