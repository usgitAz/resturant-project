from django.db import models

from accounts.models import UserModel
from menu.models import FooditemModel

class CartModel(models.Model):
    user= models.ForeignKey(UserModel , models.CASCADE)
    fooditem = models.ForeignKey(FooditemModel , models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user
    
        

class Taxmodel(models.Model):
    tax_type = models.CharField(max_length=20 , unique=True)
    tax_percentage = models.DecimalField(decimal_places=2 , max_digits=4 , verbose_name='Tax Percentage (%)')
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.tax_type
    