from django.contrib import admin

from .models import CartModel , Taxmodel

class CartAdmin(admin.ModelAdmin):
    list_display =['user' , 'fooditem' , 'quantity' , 'updated_at']

class TaxAdmin(admin.ModelAdmin):
    list_display = ['tax_type' , 'tax_percentage' , 'is_active']

admin.site.register(CartModel , CartAdmin)
admin.site.register(Taxmodel , TaxAdmin)