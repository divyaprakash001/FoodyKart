from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .context_processors import get_cart_amounts, get_cart_counter
from marketplace.models import Cart
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required

# Create your views here.
def marketplace(request):
  vendors = Vendor.objects.filter(is_approved=True, user__is_active=True).prefetch_related('category_set')[:8]
  vendor_count = vendors.count()
  context={
    'vendors':vendors,
    'vendor_count':vendor_count
  }
  return render(request,'marketplace/listings.html',context)

def vendor_detail(request,vendor_slug):
  vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
  categories = Category.objects.filter(vendor=vendor).prefetch_related(
    Prefetch(
      'fooditems',
      queryset=FoodItem.objects.filter(is_available=True)
    )
  )

  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user=request.user)
  else:
    cart_items = None

  context = {
    'vendor':vendor,
    'categories':categories,
    'cart_items':cart_items,
  }
  return render(request,'marketplace/vendor_detail.html',context)


def add_to_cart(request,food_id=None):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      # check if the food item exists
      try:
        fooditem = FoodItem.objects.get(id=food_id)
        print(fooditem)
        # check if the user already added that food to the cart
        try:
          checkCart = Cart.objects.get(user=request.user, fooditem = fooditem)
          print(checkCart)
          # increase the cart quantity
          checkCart.quantity += 1
          checkCart.save()
          return JsonResponse({"status":"Success","message":"Increase the cart quantity.","cart_counter":get_cart_counter(request),"qty":checkCart.quantity,'get_cart_amounts':get_cart_amounts(request)})
        except:
          checkCart  = Cart.objects.create(user=request.user, fooditem = fooditem, quantity=1)
          return JsonResponse({"status":"Success","message":"Added the food to the cart.","cart_counter":get_cart_counter(request),"qty":checkCart.quantity,'get_cart_amounts':get_cart_amounts(request)})
      except:
        return JsonResponse({"status":"Failed","message":"This food does not exist."})
    else:
      return JsonResponse({"status":"Failed","message":"Invalid request."})
  else:
    return JsonResponse({"status":"login_required","message":"Please login to continue"})
  

def decrease_cart(request,food_id=None):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      # check if the food item exists
      try:
        fooditem = FoodItem.objects.get(id=food_id)
        # check if the user already added that food to the cart
        try:
          checkCart = Cart.objects.get(user=request.user, fooditem = fooditem)
          # increase the cart quantity
          if  checkCart.quantity > 1:
            checkCart.quantity -= 1
            checkCart.save()
            return JsonResponse({"status":"Success","message":"Decrease the cart quantity.","cart_counter":get_cart_counter(request),"qty":checkCart.quantity,'get_cart_amounts':get_cart_amounts(request)})
          else:
            checkCart.delete()
            checkCart.quantity = 0
            return JsonResponse({"status":"Removed","message":"You have removed this item from the cart","cart_counter":get_cart_counter(request),"qty":checkCart.quantity,'get_cart_amounts':get_cart_amounts(request)})
        except Cart.DoesNotExist:
          return JsonResponse({"status":"Failed","message":"You donot have this item in your cart."})
      except:
        return JsonResponse({"status":"Failed","message":"This food does not exist."})
    else:
      return JsonResponse({"status":"Failed","message":"Invalid request."})
  else:
    return JsonResponse({"status":"login_required","message":"Please login to continue"})
  

@login_required(login_url='login')
def cart(request):
  context={}
  cart_items = Cart.objects.filter(user=request.user).order_by("created_at")
  context['cart_items'] = cart_items
  return render(request,"marketplace/cart.html",context)


def delete_from_cart(request,cart_id=None):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      print(cart_id)
      try:
        cart_item = Cart.objects.get(user=request.user,id=cart_id)
        print(cart_item)
        if cart_item:
          cart_item.delete()
          return JsonResponse({"status":"Deleted","message":"Item removed from cart.","cart_counter":get_cart_counter(request),'get_cart_amounts':get_cart_amounts(request)})
        else:
          return JsonResponse({"status":"Not Found","message":"Item not found in cart."})
      except:
        return JsonResponse({"status":"Failed","message":"Failed To Remove From Cart."})
    else:
      return JsonResponse({"status":"Invalid Request","Message":"Invalid Request"})
  else:
    return JsonResponse({"status":"Login Required","Message":"Please login to continue"})
  

def search(request):
  context={}
  rest_name=  request.GET.get("rest_name")
  address=  request.GET.get("address")
  latitude=  request.GET.get("lat")
  longitude=  request.GET.get("lng")
  radius=  request.GET.get("radius")
  print(rest_name)
  print(address)
  print(latitude)
  print(longitude)
  print(radius)

  conditions={}
  if rest_name:
    conditions['vendor_name__icontains']=rest_name
  if address:
    conditions['address__icontains']=address

  vendors =  Vendor.objects.filter(**conditions)
  context['vendors'] = vendors



      

  return render(request,"marketplace/listings.html",context)