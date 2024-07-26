from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
  list_display = ('username','email','role','is_staff','is_admin','is_superadmin','is_active')
  ordering = ('-date_joined',)
  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()


admin.site.register(User,CustomUserAdmin)