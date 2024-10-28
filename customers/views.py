from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import User, UserProfile
from orders.models import Order, OrderedFood

# Create your views here.
@login_required(login_url="login")
def cprofile(request):
  profile = get_object_or_404(UserProfile,user=request.user)
  profile_form = UserProfileForm(instance=profile)
  user_form = UserInfoForm(instance=request.user)

  if request.method == 'POST':
    user_form = UserInfoForm(request.POST,  instance=request.user)
    profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request,"Updated")
    else:
      print(user_form.errors)
      print(profile_form.errors)
  else:
    user_form = UserInfoForm(instance=request.user)
    profile_form = UserProfileForm(instance=profile)

  context = {
    'profile_form':profile_form,
    'user_form':user_form,
    'profile':profile
  }
  return render(request,"customers/cprofile.html",context)

def my_orders(request):
  context={}
  orders = Order.objects.filter(user=request.user, is_ordered = True).order_by("-created_at")
  context['orders'] = orders
  return render(request,"customers/my_orders.html",context)

def order_details(request,order_number=None):
  context={}
  try:
    order = Order.objects.get(user=request.user, order_number=order_number)
    ordered_food = OrderedFood.objects.filter(order=order)
    subtotal = 0
    for item in ordered_food:
      subtotal += (item.price * item.quantity)

    tax_data = order.tax_data

    context['order'] = order
    context['ordered_food'] = ordered_food
    context['subtotal'] = subtotal
    context['tax_data'] = tax_data
 
    return render(request,"customers/order_details.html",context)
  except:
    return redirect("customer")