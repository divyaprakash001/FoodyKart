from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .context_processors import get_cart_counter
from marketplace.models import Cart
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch

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


def add_to_cart(request,food_id):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      # check if the food item exists
      try:
        fooditem = FoodItem.objects.get(id=food_id)
        # check if the user already added that food to the cart
        try:
          checkCart = Cart.objects.get(user=request.user, fooditem = fooditem)
          # increase the cart quantity
          checkCart.quantity += 1
          checkCart.save()
          return JsonResponse({"status":"Success","message":"Increase the cart quantity.","cart_counter":get_cart_counter(request),"qty":checkCart.quantity})
        except:
          checkCart  = Cart.objects.create(user=request.user, fooditem = fooditem, quantity=1)
          return JsonResponse({"status":"Success","message":"Added the food to the cart.","cart_counter":get_cart_counter(request),"qty":checkCart.quantity})
      except:
        return JsonResponse({"status":"Failed","message":"This food does not exist."})
        pass
    else:
      return JsonResponse({"status":"Failed","message":"Invalid request."})
  else:
    
    return JsonResponse({"status":"Failed","message":"Please login to continue"})
  
