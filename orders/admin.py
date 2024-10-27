from django.contrib import admin
from .models import Payment,Order,OrderedFood

# Register your models here.
class OrderedFoodInline(admin.TabularInline):
  model=OrderedFood
  readonly_fields = ['order','payment','user','fooditem','quantity','price','amount']
  extra=0

class OrderAdmin(admin.ModelAdmin):
  list_display = ['order_number','payment','user','email','total','is_ordered','status','updated_at']
  inlines = [OrderedFoodInline]

class OrderedFoodAdmin(admin.ModelAdmin):
  list_display = ['fooditem','quantity','price','amount','user','payment','order','updated_at']

class PaymentAdmin(admin.ModelAdmin):
  list_display = ['transaction_id','user','payment_method','amount','status','created_at']


admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood,OrderedFoodAdmin)