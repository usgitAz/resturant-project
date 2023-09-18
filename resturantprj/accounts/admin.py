from django.contrib import admin
from .models import UserModel , UserProfileModel
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# class UsersAdmin(admin.ModelAdmin):
#     readonly_fields =['password']


class customUsersAdmin(UserAdmin):
    list_display = ('email', 'username' , 'first_name' , 'last_name', 'role' , 'is_active')
    ordering=('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(UserModel , customUsersAdmin)
admin.site.register(UserProfileModel)

