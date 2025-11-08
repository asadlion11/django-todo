from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Todo

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # form fields
        fields= ['first_name', 'last_name','username']
        
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'is_complete']
    
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50,widget=forms.PasswordInput)