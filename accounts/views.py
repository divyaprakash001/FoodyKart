from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from vendor.models import Vendor
from django.contrib import messages,auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# restrict the vendor from accessing customer page
def check_role_vendor(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied


# restrict the customer from accessing vendor page
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied





def registerUser(request):
  if request.user.is_authenticated:
    messages.warning(request,'You have already logged in!')
    return redirect('myAccount')
  elif(request.method == "POST"):
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
  if request.user.is_authenticated:
    messages.warning(request,'You have already logged in!')
    return redirect('myAccount')
  elif request.method=='POST':
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

def login(request):
  if request.user.is_authenticated:
    messages.warning(request,'You have already logged in!')
    return redirect('myAccount')
  elif request.method == 'POST':
      email  = request.POST['email']
      password  = request.POST['password']
      user = auth.authenticate(email=email, password=password)
      # print(user)
      if user is not None:
        auth.login(request, user)
        messages.success(request, 'You are successfully logged in. Enjoy your meal.')
        return redirect("myAccount")
      else:
        messages.error(request,'Invalid login credentials.')
        return redirect("login")
  else:
    return render(request,"accounts/login.html")


@login_required(login_url='login')
def logout(request):
  auth.logout(request)
  messages.info(request,"You are now logged out.")
  return redirect("login")


@login_required(login_url='login')
def myAccount(request):
  user  = request.user
  redirectUrl = detectUser(user)
  return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
  return render(request,'accounts/customerDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
  return render(request,'accounts/vendorDashboard.html')

