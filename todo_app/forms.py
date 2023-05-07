from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        # fields = '__all__'
        exclude = ["user", "is_completed", 'updated',]
        
class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        # fields = '__all__'
        exclude = ["user",]
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)
    
class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)