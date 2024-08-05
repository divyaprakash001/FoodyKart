from django.contrib import admin
from .models import Vendor
# Register your models here.
class VendorAdmin(admin.ModelAdmin):
  list_display = ['vendor_name','user','is_approved']
  list_filter = ['is_approved','created_at','modified_at']


admin.site.register(Vendor,VendorAdmin)