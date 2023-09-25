from django import forms
from .models import CategoryModel

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