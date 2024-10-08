from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from REMS.models import *


class LoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100)


class RegForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']


from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['category', 'description', 'price', 'image', 'country', 'state', 'city', 'address']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a category'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter property description',
                'style': 'resize: none;'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price in $',
                'min': '0'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full address'
            }),
        }
        labels = {
            'category': 'Property Category',
            'description': 'Property Description',
            'price': 'Price ($)',
            'image': 'Upload Image',
            'country': 'Country',
            'state': 'State/Region',
            'city': 'City',
            'address': 'Full Address',
        }



class ProfileForm(forms.Form):
    profile_pic = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell us about yourself',
            'style': 'resize: none;'
        })
    )
    first_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    phone = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
            'min': '0'
        })
    )

  

class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Message')

class SearchForm(forms.Form):
    search=forms.CharField(max_length=100)