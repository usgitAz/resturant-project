from django.contrib import admin

from .models import CartModel

class CartAdmin(admin.ModelAdmin):
    list_display =['user' , 'fooditem' , 'quantity' , 'updated_at']


admin.site.register(CartModel , CartAdmin)