from registration.forms import RegistrationFormUniqueEmail
from django import forms
from .models import Consumer, ShopKeeper
from collections import OrderedDict


class UserRegForm(RegistrationFormUniqueEmail):
    """add check about type of registration"""
    type = forms.BooleanField(label='As Shop Keeper? ',
                              initial=False, required=False)


class BaseProf(forms.ModelForm):
    email = forms.EmailField(disabled=True, label='Register Email')
    username = forms.CharField(
        max_length=30, disabled=True, label='Login Name')
    datejoined = forms.DateField(disabled=True, label='Date Registered')

    def __init__(self, *args, **kwargs):
        super(BaseProf, self).__init__(*args, **kwargs)
        self.initial['email'] = self.instance.user.email
        self.initial['username'] = self.instance.user.username
        self.initial['datejoined'] = self.instance.user.date_joined
        fields = OrderedDict()
        for key in ('username', 'email', 'datejoined'):
            fields[key] = self.fields.pop(key)
        for key, value in self.fields.items():
            fields[key] = value
        self.fields = fields


class ConsumerProf(BaseProf):

    class Meta:
        model = Consumer
        exclude = ('user',)
        labels = {
            'dftAddress': 'Default Address',
            'dftPayType': 'Default Paying Method'
        }


class ShopKeeperProf(BaseProf):

    class Meta:
        model = ShopKeeper
        exclude = ('user', 'shop')
        labels = {
            'account': 'Shroff Account',
        }
