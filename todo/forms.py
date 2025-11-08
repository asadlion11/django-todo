from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Todo

# Two types of Django forms:
# 1. ModelForm - When you HAVE a model
# 2. Form - When you DON'T have a model 

class CustomUserCreationForm(UserCreationForm):
    #  metadata
    class Meta:
        model = User
        # form fields
        fields= ['first_name', 'last_name','username']
        # UserCreationForm automatically includes password fields(password & confirm password)
        
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'is_complete']
    
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50,widget=forms.PasswordInput)