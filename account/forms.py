from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')



class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'fb_social', 'twitter_social', 'phone_number', 'gender',  'short_bio', 'address', 'billing_address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'profile__input', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'profile__input  ', 'placeholder': 'Enter your email'}),
            'fb_social': forms.URLInput(attrs={'class': 'profile__input', 'placeholder': 'Enter your Facebook URL'}),
            'twitter_social': forms.URLInput(attrs={'class': 'profile__input', 'placeholder': 'Enter your Twitter URL'}),
            'phone_number': forms.TextInput(attrs={'class': 'profile__input', 'placeholder': 'Enter your phone number'}),
            'gender': forms.Select(attrs={'class': 'profile__input nice-select open'}),
            'short_bio': forms.Textarea(attrs={'class': 'profile__input col-lg-12', 'placeholder': 'Enter a short bio'}),
            'address': forms.Textarea(attrs={'class': 'profile__input col-lg-12', 'placeholder': 'Enter a address'}),
            'billing_address': forms.Textarea(attrs={'class': 'profile__input col-lg-12', 'placeholder': 'Enter a billing adress'}),
        }