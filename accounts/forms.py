from django import forms
from . import models

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  confirm_password = forms.CharField(widget=forms.PasswordInput())
  alternate_number = forms.CharField()
  class Meta:
    model = models.User
    fields = ['first_name','last_name','username','email','phone_number','password']

  def clean(self):
    cleaned_data = super(UserForm,self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
      raise forms.ValidationError(
        "Password does not match!"
      )
    # this validation is called non-field error
        
       
    