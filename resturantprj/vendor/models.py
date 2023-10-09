from django.db import models
from accounts.models import UserModel , UserProfileModel
from accounts.Utils import send_notification_email
from datetime import time , date , datetime
# Create your models here.


class VendorModel(models.Model):
    vendoruser= models.OneToOneField(UserModel , related_name='UserModel'  , on_delete=models.CASCADE )
    vendor_profile = models.OneToOneField(UserProfileModel , related_name='UserProfileModel' , on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_slug = models.SlugField(max_length=100  , unique=True)
    vendor_license = models.FileField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.vendor_name}"
    
    def is_open(self):
        today = date.today().isoweekday()
        current_day = OpeningHourModel.objects.filter(vendor = self , day = today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        is_open = None
        for i in current_day :
            if not i.is_closed :
                strart_time = str(datetime.strptime(i.from_hour , "%I:%M %p").time())
                end_time = str(datetime.strptime(i.to_hour , "%I:%M %p").time() )
                if current_time > strart_time and current_time < end_time :
                    is_open = True
                    break
                else :
                    is_open = False
        return is_open
    
    def save(self , *args, **kwargs):
        if self.pk is not None:
            account = VendorModel.objects.get(pk=self.pk)
            if account.is_approved != self.is_approved :
                mail_template = 'accounts/emails/admin_approval_email.html'

                context = {
                        'user' : self.vendoruser ,
                        'is_approved' : self.is_approved,
                        'to_email' : self.vendoruser.email,
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


DAYS = [ 
    (1 , ('Monday')), 
    (2 , ('Tuesday')), 
    (3 , ('Wednesday')), 
    (4 , ('Thursday')), 
    (5 , ('Friday')), 
    (6 , ('Saturday')), 
    (7 , ('Sunday')) 
]

HOUR_OF_DAY = [(time(h , m).strftime('%I:%M %p') , time(h , m).strftime('%I:%M %p' )) for h in range(0 ,24) for m in (0,30) ]

class OpeningHourModel(models.Model):
    vendor = models.ForeignKey(VendorModel , on_delete=models.CASCADE)
    day =models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY , blank=True , max_length=10)
    to_hour = models.CharField(choices=HOUR_OF_DAY , blank=True , max_length=10)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering= ('day', '-from_hour')
        unique_together = ('vendor','day' , 'from_hour' , 'to_hour')

    def __str__(self):
        return self.get_day_display() #show the day with get display to see the labels
    