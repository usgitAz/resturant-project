from django.contrib import admin
from .models import OrderModel , OrderedFoodModel , PaymentModel
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number' , 'user' , 'status' , 'is_ordered')

admin.site.register(PaymentModel)
admin.site.register(OrderModel , OrderAdmin)
admin.site.register(OrderedFoodModel)