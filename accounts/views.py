from django.shortcuts import render, redirect

from orders.models import Order
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from vendor.models import Vendor
from django.contrib import messages,auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import  urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.text import slugify


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

      # send verification email
      mail_subject = 'Please activate your account.'
      email_template = 'accounts/emails/account_verification_email.html'
      send_verification_email(request,user,mail_subject,email_template)

      messages.success(request, "Your account has been registered successfully! Please check your email for activation link.")
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
      vendor_name =v_form.cleaned_data['vendor_name']
      user_profile = UserProfile.objects.get(user=user)
      vendor.user_profile = user_profile
      vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
      vendor.save()
      print(vendor.id)

      # sending the email verification
      mail_subject = 'Please activate your account.'
      email_template = 'accounts/emails/account_verification_email.html'
      send_verification_email(request,user,mail_subject,email_template)
      # vendor created
      messages.success(request, "Your account has been registered successfully! Please check your email for activation link.")
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

def activate(request,uidb64,token):
  # activate the user by sending the is_active status to true
  try:
   uid = urlsafe_base64_decode(uidb64).decode()
   user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  
  if user is not None and default_token_generator.check_token(user,token):
    user.is_active = True
    user.save()
    messages.success(request,'Congratulations! Your account is activated.')
    return redirect('myAccount')
  else:
    messages.error(request,'Invalid activation link')
    return redirect('myAccount')


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
  

  
# done by myself
# def forgotPassword(request):
#   if request.method=='POST':
#     email  = request.POST.get('email')
#     user = User.objects.get(email__exact=email)
#     print("yaha aya")
#     if user is not None:
#       print("yaha aya 2")
#       send_reset_email(request,user)
#       print("yaha aya 3")
#       messages.success(request,'Reset link sent on your email.')
#       return redirect('login')
#     else:
#       messages.error(request,'User doesnot exist on given email!')
#   else:
#     return render(request,"accounts/forgotPassword.html")
  
# def resetPassword(request,uidb64,token):
#   if request.method=='POST':
#     password = request.POST['password']
#     try:
#       uid = urlsafe_base64_decode(uidb64).decode()
#       user = User._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#       user = None
    
#     if user is not None and default_token_generator.check_token(user,token):
#       user.set_password(password)
#       user.save()
#       messages.success(request,'Congratulations! Your password has been reset.')
#       return redirect("login")

#   # activate the user by sending the is_active status to true
#   else:
#     try:
#       uid = urlsafe_base64_decode(uidb64).decode()
#       user = User._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#       user = None
    
#     if user is not None and default_token_generator.check_token(user,token):
#       return render(request,"accounts/resetPassword.html")
#     else:
#       messages.error(request,'Invalid reset link')
#       return redirect('forgotPassword')


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
  context={}
  orders = Order.objects.filter(user=request.user, is_ordered = True)
  orders_count = orders.count()
  recent_orders = orders.order_by("-created_at")[:5]
  context['orders'] = orders
  context['recent_orders'] = recent_orders
  context['orders_count'] = orders_count
  return render(request,'accounts/customerDashboard.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
  context={}
  vendor = Vendor.objects.get(user=request.user)
  orders = Order.objects.filter(vendors__in = [vendor.id],is_ordered=True).order_by("-created_at")
  recent_orders = orders[:5]
  context['orders'] = orders
  context['order_count'] = orders.count()
  context['recent_orders'] = recent_orders
  return render(request,'accounts/vendorDashboard.html',context)

def forgot_password(request):
  if request.method == 'POST':
    email = request.POST['email']

    if User.objects.filter(email=email).exists():
      user = User.objects.get(email__exact=email)

      # send reset password
      mail_subject = 'Reset Your Password'
      # email_template = 'accounts/emails/account_verification_email.html'
      email_template = 'accounts/emails/account_passwordReset_email.html'
      send_verification_email(request, user, mail_subject, email_template)

      messages.success(request,'Password reset link has been sent to your email address.')
      return redirect('login')
    else:
      messages.error(request,'Account doesnot exist.')
      return redirect('forgot_password')
  return render(request,"accounts/forgotPassword.html")

def reset_password_validate(request, uidb64, token):
  # validate the user by decoding the token and user pk
  try:
   uid = urlsafe_base64_decode(uidb64).decode()
   user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  
  if user is not None and default_token_generator.check_token(user,token):
    request.session['uid'] = uid
    messages.info(request,'Please reset your password.')
    return redirect('reset_password')
  else:
    messages.error(request,'This link has been expired.')
    return redirect('myAccount')

def reset_password(request):
  if request.method=='POST':
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if password == confirm_password:
      uid = request.session.get('uid')
      user = User.objects.get(pk=uid)
      user.set_password(password)
      user.is_active=True
      user.save()
      messages.success(request,'Password reset successful.')
      return redirect("login")
    else:
      messages.error(request,'Password do not match')
      return redirect(reset_password)

 
  return render(request,"accounts/resetPassword.html")