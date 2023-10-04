from typing import Any, Dict
from django import forms
from .models import UserModel , UserProfileModel
from .validators import allow_only_images_validator

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


class UserProfileForm(forms.ModelForm):
    # set css class to form input
    address = forms.CharField(widget=forms.TextInput(attrs={'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'readonly':'readonly'}) , validators=[allow_only_images_validator])
    cover_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn.btn-info'}) , validators=[allow_only_images_validator])

    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfileModel
        exclude = ['user' , 'creat_at' , 'modified_at']
        error_messages = {
        
        }
        

    def __init__ (self , *args, **kwargs):
        super(UserProfileForm , self ).__init__(*args, **kwargs)
        for field in self.fields:
            if field  == 'latitude' or field == 'longtitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                self.fields['latitude'].required = False
                self.fields['longitude'].required = False



class UserInforForm(forms.ModelForm):
    class Meta:
        model = UserModel 
        fields = ['first_name' , 'last_name']