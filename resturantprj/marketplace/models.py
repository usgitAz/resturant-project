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
    
        