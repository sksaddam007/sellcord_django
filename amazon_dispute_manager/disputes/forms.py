# disputes/forms.py

from django import forms
from .models import Item, Order, Return, Dispute, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'item', 'date_ordered']


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['order', 'return_reason', 'return_tracking', 'date_returned']


class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ['dispute_reason', 'status', 'resolution_details']
