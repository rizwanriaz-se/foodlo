from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

#User Registration Form
class RegisterForm(UserCreationForm):

    username = forms.CharField(required=True,
                               label='',
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Enter your name',
                                       'required': ''
                                   }))
    email = forms.CharField(required=True,
                            label='',
                            widget=forms.EmailInput(
                                attrs={
                                    'placeholder': 'Enter your email',
                                    'required': ''
                                }))
    password1 = forms.CharField(required=True,
                                label='',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': 'Enter password',
                                        'required': ''
                                    }))
    password2 = forms.CharField(required=True,
                                label='',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': 'Confirm password',
                                        'required': ''
                                    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'class': 'input-field'})}


#User Login form
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={
            'autofocus': True,
            'required': '',
            'placeholder': 'Enter your username'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'required': '',
            'placeholder': 'Enter your password'
        }))