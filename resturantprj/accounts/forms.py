from typing import Any, Dict
from django import forms
from .models import UserModel

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=UserModel
        fields=['username', 'first_name' , 'last_name' , 'email' , 'password']
        error_messages = {
            "email" :{
                "unique" : "This email already exists !",
                "required" : "Please Enter your email !"
            },
             "username" :{
                "unique" : "This username already exists !",
                "required": "Please Enter username "
            },
            "first_name" :{
                "required": "Please Enter your Fisrtname ! "
            },
            "last_name" :{
                "required": "Please Enter your Lastname ! "
            },
            "password" :{
                "required": "Enter your password !"
            },

        }
    
    def clean(self):
        cleaned_date = super(UserForm , self).clean()
        password = cleaned_date.get("password")
        confirm_password =cleaned_date.get('confirm_password')

        if password != confirm_password :
            raise forms.ValidationError('Password dosent match !')
