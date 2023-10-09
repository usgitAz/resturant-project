from django.contrib import admin
from .models import OrderModel , OrderedFoodModel , PaymentModel
# Register your models here.


class OrderedFoodInline(admin.TabularInline): #for show information with tablure inline
    model = OrderedFoodModel
    extra = 0 #dont add extra empty field in admin panel  
    readonly_fields = ('order' , 'payment' , 'user' , 'fooditem' , "quantity" , "price" ,"amount")

class OrederAdmin(admin.ModelAdmin):
    list_display = ['order_number' , 'name' ,'phone', 'email' , 'total' , 'payment_method' , 'status' , 'is_ordered']
    inlines = [OrderedFoodInline]



admin.site.register(PaymentModel)
admin.site.register(OrderModel , OrederAdmin)
admin.site.register(OrderedFoodModel)