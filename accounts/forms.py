from django import forms
from .models import User,UserProfile
from accounts.validators import allow_only_images_validator

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
  alternate_number = forms.CharField()
  class Meta:
    model = User
    fields = ['first_name','last_name','username','email','phone_number','password']
    widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }

  def clean(self):
    cleaned_data = super(UserForm,self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
      raise forms.ValidationError(
        "Password does not match!"
      )
    # this validation is called non-field error
        
class UserProfileForm(forms.ModelForm):
  profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
  cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
  address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter a Place','required':'required'}))
  class Meta:
    model = UserProfile
    fields = ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longtitude']    
    widgets = {
            # 'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            # 'address_line_2': forms.TextInput(attrs={'placeholder': 'Address Line 1'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'pin_code': forms.TextInput(attrs={'placeholder': 'Pin Code'}),
            # 'latitude': forms.TextInput(attrs={'placeholder': 'Latitude','readonly':'readonly'}),
            # 'longtitude': forms.TextInput(attrs={'placeholder': 'Longitude','readonly':'readonly'}),
            # 'cover_photo':forms.FileInput(attrs={'class':'btn btn-info','accept': 'image/*'}),
        }
  # def __init__(self,*args, **kwargs):
  #   super(UserProfileForm,self).__init__(*args, **kwargs)
  #   for field in self.fields:
  #     if field == 'latitude' or field == 'longtitude':
  #       self.fields[field].widget.attrs['readonly'] = 'readonly'

      # if field == 'profile_picture' or field == 'cover_photo':
      #   self.fields[field].widget.attrs['class'] = 'btn btn-info'
      #   self.fields[field].validators = [allow_only_images_validator]

class UserInfoForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name','last_name','phone_number']