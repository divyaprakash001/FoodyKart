from django.shortcuts import render, redirect
from . import forms
from . import models
from django.contrib import messages

# Create your views here.
def registerUser(request):
  if(request.method == "POST"):
    form  = forms.UserForm(request.POST)
    if form.is_valid():
      # create the user using the form
    
      # user = form.save(commit=False)
      # password = form.cleaned_data['password']
      # user.set_password(password)
      # user.role = models.User.CUSTOMER 
      # user = form.save()

      # create user using create_user method
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      user = models.User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      user.role = models.User.CUSTOMER
      print("user is created")
      user.save()
      messages.success(request, "Your account has been registered successfully!")
      return redirect('registerUser')
    else:
      print("Invalid form")
      print(form.errors)
  else:
    form= forms.UserForm()
  context = {
      "form":form
  }
  return render(request,"accounts/registerUser.html",context)