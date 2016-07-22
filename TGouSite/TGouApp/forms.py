from registration.forms import RegistrationForm
from django import forms
from .models import Consumer, ShopKeeper


class UserRegForm(RegistrationForm):
    """add check about type of registration"""
    type = forms.BooleanField(label='As Shop Keeper? ', initial=False, required=False)
