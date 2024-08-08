from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from vendor.models import Vendor
from django.contrib import messages

# Create your views here.
def registerUser(request):
  if(request.method == "POST"):
    form  = UserForm(request.POST)
    if form.is_valid():
      # create the user using the form
    
      # user = form.save(commit=False)
      # password = form.cleaned_data['password']
      # user.set_password(password)
      # user.role = User.CUSTOMER 
      # user = form.save()

      # create user using create_user method
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      user.role = User.CUSTOMER
      print("user is created")
      user.save()
      messages.success(request, "Your account has been registered successfully!")
      return redirect('registerUser')
    else:
      print("Invalid form")
      print(form.errors)
  else:
    form= UserForm()
  context = {
      "form":form
  }
  return render(request,"accounts/registerUser.html",context)

def registerVendor(request):
  if request.method=='POST':
    form = UserForm(request.POST)
    v_form = VendorForm(request.POST,request.FILES)
    if form.is_valid() and v_form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']

      # create user as per our definition
      user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      user.role = User.VENDOR
      user.save()
      print("user created")
      # form for vendor
      vendor = v_form.save(commit=False)
      vendor.user = user
      user_profile = UserProfile.objects.get(user=user)
      vendor.user_profile = user_profile
      vendor.save()
      # vendor created
      messages.success(request, "Your account has been registered successfully! Please wait for the approval.")
      return redirect('registerVendor')
    else:
      print("Invalid form")
      print(form.errors)
  else:
    form = UserForm()
    v_form = VendorForm(request.POST)
  context = {
    "form":form,
    "v_form":v_form,
  }
  return render(request,'accounts/registerVendor.html',context)