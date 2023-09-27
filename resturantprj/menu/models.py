from django.db import models
from vendor.models import VendorModel
# Create your models here.

class CategoryModel(models.Model):
    vendor = models.ForeignKey(VendorModel , on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50 , unique=True)
    slug = models.SlugField(max_length=100 , unique=True)
    description = models.TextField(max_length=250 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        self.category_name = self.category_name.lower()

    def __str__(self):
        return f"{self.category_name}"
    

class FooditemModel(models.Model):
    vendor = models.ForeignKey(VendorModel , on_delete=models.CASCADE)
    category= models.ForeignKey(CategoryModel,  on_delete=models.CASCADE , related_name='fooditems')
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100 , unique=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    description = models.TextField(max_length=250 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_title

    