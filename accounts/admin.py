from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):

  # these top three lines make the password non editable
  filter_horizontal = ()
  list_filter= ()
  fieldsets=()

  list_display = ['email','first_name','last_name', 'username' ,'role','is_active']
  list_filter = ['date_joined','modified_date','created_date', 'role','is_active']
  ordering = ['-date_joined']
  list_editable = ['is_active']




# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)