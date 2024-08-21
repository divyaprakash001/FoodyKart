from django.shortcuts import render, get_object_or_404,redirect
from vendor.models import Vendor
from vendor.forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.views import check_role_vendor
from menu.models import Category,FoodItem
from .utils import get_vendor
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify




# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
  profile = get_object_or_404(UserProfile,user=request.user)
  vendor = get_object_or_404(Vendor, user=request.user)

  if request.method == 'POST':
    profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
    vendor_form = VendorForm(request.POST,request.FILES,instance=vendor)
    if profile_form.is_valid() and vendor_form.is_valid():
      profile_form.save()
      vendor_form.save()
      messages.success(request,'Profile updated.')
      return redirect('vprofile')
    else:
      print(profile_form.errors)
      print(vendor_form.errors)
  else:
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)
  context={
    'profile_form':profile_form,
    'vendor_form':vendor_form,
    'profile':profile,
    'vendor':vendor
    }
  return render(request,'vendor/vprofile.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
  vendor = get_vendor(request)
  categories = Category.objects.filter(vendor=vendor).order_by("created_at")

  context={
    'categories':categories,
  }
  return render(request,"vendor/menu_builder.html", context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
  vendor = vendor = get_vendor(request)
  category = get_object_or_404(Category, pk = pk)
  fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
  print(fooditems)
  context = {
    'category':category,
    'fooditems':fooditems,
  }
  return render(request,"vendor/fooditems_by_category.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      category_name = form.cleaned_data['category_name']
      category  = form.save(commit=False)
      category.vendor= get_vendor(request)
      category.slug = slugify(category_name)
      form.save()
      messages.success(request,"Category Added Successfully.")
      return redirect("menu_builder")
    else:
      print(form.errors)
  else:
    form = CategoryForm()
  context={
    'form':form
  }
  return render(request,"vendor/add_category.html",context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,id=None):
  category  = get_object_or_404(Category,pk=id)
  if request.method == 'POST':
    form = CategoryForm(request.POST,instance=category)
    if form.is_valid():
      category_name = form.cleaned_data['category_name']
      category  = form.save(commit=False)
      category.vendor= get_vendor(request)
      category.slug = slugify(category_name)
      form.save()
      messages.success(request,"Category Updated Successfully.")
      return redirect("menu_builder")
    else:
      print(form.errors)
  else:
    form = CategoryForm(instance=category)
  context={
    'form':form,
    'category':category
  }
  return render(request,"vendor/edit_category.html",context)
  



def delete_category(request,id=None):
  vendor = vendor = get_vendor(request)
  category = get_object_or_404(Category, pk = id)
  category.delete()
  messages.success(request,"Category Deleted Successfully.")
  return redirect("menu_builder")