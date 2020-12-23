from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 
                        'placeholder': 'Enter Student Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 
                        'placeholder': 'Enter Student Email ID'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 
                        'placeholder': 'Enter Password'}),
        }

class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 
                        'placeholder': 'Enter Student Name'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 
                        'placeholder': 'Enter Password'}),
        }