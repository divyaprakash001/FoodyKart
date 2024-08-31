from django.shortcuts import render
from django.http import HttpResponse

from vendor.models import Vendor

# Create your views here.
def home(request):
  vendors = Vendor.objects.filter(is_approved=True, user__is_active=True).prefetch_related('category_set')[:8]
  
  context={
    "vendors":vendors
  }
  return render(request, "home.html",context)