from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)
        
class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields 
        
class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)