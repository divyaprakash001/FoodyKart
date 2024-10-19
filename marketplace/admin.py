from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
  list_display = ['fooditem','user','quantity','updated_at','id']

# Register your models here.
admin.site.register(Cart,CartAdmin)