from django.shortcuts import render
from vendor.models import Vendor

# Create your views here.
def vprofile(request):
  return render(request,'vendor/vprofile.html')