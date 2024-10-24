from django import forms

class ProfileForm(forms.Form):
  class Meta:
    model = 'Profile'
    fields = ['__all__']