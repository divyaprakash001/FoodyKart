from django.contrib import admin
from .models import Cart, Tax

class CartAdmin(admin.ModelAdmin):
  list_display = ['fooditem','user','quantity','updated_at','id']

class TaxAdmin(admin.ModelAdmin):
  list_display = ['tax_type','tax_percentage','is_active','id']

# Register your models here.
admin.site.register(Cart,CartAdmin)
admin.site.register(Tax,TaxAdmin)