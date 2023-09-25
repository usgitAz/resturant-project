from django.contrib import admin
from .models import CategoryModel , FooditemModel
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug' : ('category_name',)}
    list_display = ('category_name' , 'vendor' , 'updated_at')
    list_display_links = ('category_name', 'vendor' ,)
    search_fields = ('category_name','vendor__vendor_name')
    ordering=('created_at',)


class FooditemAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug' : ('food_title',)}
    list_display = ('food_title' ,'category' , 'vendor' ,'price','is_available' ,'updated_at')
    search_fields = ('food_title','category__category_name','vendor__vendor_name', 'price')
    list_filter = ("is_available" ,)

admin.site.register(CategoryModel , CategoryAdmin)
admin.site.register(FooditemModel , FooditemAdmin)