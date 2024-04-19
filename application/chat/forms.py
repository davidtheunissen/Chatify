from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

# New user registration form
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
       
# Chat message box form 
class ChatMessageForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'class': 'form-control py-2 px-2', 'rows': '1', 'autofocus': True, 'placeholder': 'Type your message'})
        }