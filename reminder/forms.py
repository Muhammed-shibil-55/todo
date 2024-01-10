from django import forms

from reminder.models import Todos
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    password1=forms.CharField(label="password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label="confirm password",widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
        

        }


class SignInForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todos
        fields=["name"]
        
