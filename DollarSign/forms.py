from django import forms
from .models import Stock
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker', 'shares', 'purchase_date']
