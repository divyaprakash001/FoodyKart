from django.contrib import admin
from .models import Category, FoodItem

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('category_name',)}
  list_display=['category_name','vendor','updated_at']
  list_display_links = ['vendor','category_name']
  search_fields = ['category_name','vendor__vendor_name']
  list_filter=['created_at','updated_at']



class FoodItemAdmin(admin.ModelAdmin):
  list_display=['food_title','category','vendor','price','is_available','updated_at']
  list_display_links = ['food_title','vendor','category','price']
  list_editable = ['is_available']
  search_fields = ['category__category_name','food_title','vendor__vendor_name','price']

  prepopulated_fields = {'slug': ('food_title',)}


admin.site.register(Category,CategoryAdmin)
admin.site.register(FoodItem,FoodItemAdmin)
