from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import LoginModel
from django.forms import ModelForm



class SignupForm(UserCreationForm):

    mobile = forms.IntegerField()
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'mobile', 'age']

class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = LoginModel
        fields =['username', 'password']










