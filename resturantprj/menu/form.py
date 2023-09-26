from django import forms
from .models import CategoryModel, FooditemModel
from accounts.validators import allow_only_images_validator
class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = CategoryModel
        fields = ['category_name', 'description']
        error_messages = {
         "category_name" :{
                "unique" : "This category already exists !",
                "required" : "Please Enter your category Name !"
            },
        }

class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info '}) , validators=[allow_only_images_validator])
    class Meta:
        model = FooditemModel
        fields = [ 'category','food_title' , 'price' , 'image' , 'is_available' , 'description']
        error_messages = {
            "food_title" :{
                "required" : "Please Enter your Food Name !",
            },
        }
        