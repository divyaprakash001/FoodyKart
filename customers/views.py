from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import User, UserProfile

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