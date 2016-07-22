from registration.forms import RegistrationFormUniqueEmail
from django import forms
from .models import Consumer, ShopKeeper


class UserRegForm(RegistrationFormUniqueEmail):
    """add check about type of registration"""
    type = forms.BooleanField(label='As Shop Keeper? ', initial=False, required=False)

class ConsumerProf(forms.ModelForm):
    class Meta:
        model = Consumer
        exclude = ('user',)

class ShopKeeperProf(forms.ModelForm):
    class Meta:
        model = ShopKeeper
        exclude = ('user',)
