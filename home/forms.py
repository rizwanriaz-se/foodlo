from django import forms
from django.contrib.auth.models import User
from .models import UserInfo
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class RegisterForm(UserCreationForm):

    username = forms.CharField(required=True,
                               label='',
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'input-field',
                                       'placeholder': 'Enter your name',
                                       'required': ''
                                   }))
    email = forms.CharField(required=True,
                            label='',
                            widget=forms.EmailInput(
                                attrs={
                                    'class': 'input-field',
                                    'placeholder': 'Enter your email',
                                    'required': ''
                                }))
    password1 = forms.CharField(required=True,
                                label='',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'input-field',
                                        'placeholder': 'Enter password',
                                        'required': ''
                                    }))
    password2 = forms.CharField(required=True,
                                label='',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'input-field',
                                        'placeholder': 'Confirm password',
                                        'required': ''
                                    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'class': 'input-field'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={
            'autofocus': True,
            'class': 'input-field',
            'required': '',
            'placeholder': 'Enter your username'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input-field',
            'required': '',
            'placeholder': 'Enter your password'
        }))


class UserInfoForm(forms.ModelForm):
    firstname = forms.CharField(label="First Name",
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'checkoutInputs',
                                        'required': '',
                                        'placeholder': 'Enter first name'
                                    }))
    lastname = forms.CharField(label="Last Name",
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'checkoutInputs',
                                       'required': '',
                                       'placeholder': 'Enter last name'
                                   }))
    address = forms.CharField(label="Street Address",
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'checkoutInputs',
                                      'required': '',
                                      'placeholder': 'Enter your address'
                                  }))
    city = forms.CharField(label="City/Town",
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'checkoutInputs',
                                   'required': '',
                                   'placeholder': 'Enter your town'
                               }))
    zip = forms.CharField(label="Postcode/Zip",
                          widget=forms.TextInput(
                              attrs={
                                  'class': 'checkoutInputs',
                                  'required': '',
                                  'placeholder': 'Enter your postcode'
                              }))
    phone = forms.CharField(label="Phone Number",
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'checkoutInputs',
                                    'required': '',
                                    'placeholder': 'Enter phone number'
                                }))
    email = forms.EmailField(label="Enter email",
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'checkoutInputs',
                                     'required': '',
                                     'placeholder': 'Enter email'
                                 }))

    class Meta:
        model = UserInfo
        fields = [
            'firstname', 'lastname', 'address', 'city', 'zip', 'phone', 'email'
        ]


"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "required": "",
            "name": "username",
            "id": "username",
            "type": "text",
            "class": "form-input",
            "placeholder": "Username",
            "maxlength": "64",
            "minlength": "6"
        })
        self.fields["email"].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'placeholder':'JohnDoe@mail.com',
        })
        self.fields["password1"].widget.attrs.update({
            "required": "",
            "name": "password1",
            "id": "password1",
            "type": "password",
            "class": "form-input",
            "placeholder": "Password",
            "maxlength": "22",
            "minlength": "8"
        })
        self.fields["password2"].widget.attrs.update({
            "required": "",
            "name": "username",
            "id": "password",
            "type": "password",
            "class": "form-input",
            "placeholder": "Password",
            "maxlength": "22",
            "minlength": "8"
        })

    class Meta:
        model = User
        fields = ('username','email','password1','password2',)
"""
"""
class RegisterForm(forms.Form):
      username= forms.CharField(widget= forms.TextInput(attrs={ 
          'class': 'form-input', 
          'required':'', 
          'name':'username', 
          'id':'username', 
          'type':'text', 
          'placeholder':'John Doe', 
          'maxlength': '24', 
          'minlength': '6', 
			}  
    ))
      email= forms.EmailField(widget= forms.EmailInput(attrs={ 
          'class': 'form-input', 
          'required':'', 
          'name':'email', 
          'id':'email', 
          'type':'email', 
          'placeholder':'example@gmail.com'
			}  
    ))
      password1= forms.PasswordInput(attrs={ 
          'class': 'form-input', 
          'required':'', 
          'name':'password1', 
          'id':'password1', 
          'type':'password', 
          'placeholder':'Password', 
          'maxlength': '24', 
          'minlength': '6', 
			}  
    )
username= forms.CharField(widget= forms.TextInput(attrs={ 
          'class': 'form-input', 
          'required':'', 
          'name':'username', 
          'id':'username', 
          'type':'text', 
          'placeholder':'John Doe', 
          'maxlength': '24', 
          'minlength': '6', 
			}  
    ))
"""
