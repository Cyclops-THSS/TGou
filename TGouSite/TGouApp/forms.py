from registration.forms import RegistrationFormUniqueEmail
from django import forms
from .models import *
from collections import OrderedDict


class UserRegForm(RegistrationFormUniqueEmail):
    """add check about type of registration"""
    type = forms.BooleanField(label='As Shop Keeper? ',
                              initial=False, required=False)


class BaseUserProf(forms.ModelForm):
    email = forms.EmailField(disabled=True, label='Register Email')
    username = forms.CharField(
        max_length=30, disabled=True, label='Login Name')
    datejoined = forms.DateField(disabled=True, label='Date Registered')

    def __init__(self, *args, **kwargs):
        super(BaseUserProf, self).__init__(*args, **kwargs)
        self.initial['email'] = self.instance.user.email
        self.initial['username'] = self.instance.user.username
        self.initial['datejoined'] = self.instance.user.date_joined
        fields = OrderedDict()
        for key in ('username', 'email', 'datejoined'):
            fields[key] = self.fields.pop(key)
        for key, value in self.fields.items():
            fields[key] = value
        self.fields = fields


class ConsumerProf(BaseUserProf):

    class Meta:
        model = Consumer
        exclude = ('user',)
        labels = {
            'dftAddress': 'Default Address',
            'dftPayType': 'Default Paying Method'
        }


class ShopKeeperProf(BaseUserProf):

    class Meta:
        model = ShopKeeper
        exclude = ('user', 'shop')
        labels = {
            'account': 'Shroff Account',
        }


class ShopForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)
        self.fields['createDate'].widget.attrs['readonly'] = True

    class Meta:
        model = Shop
        fields = '__all__'


class OrderForm(forms.ModelForm):
    shopName = forms.CharField(max_length=200, disabled=True)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['time'].widget.attrs['readonly'] = True
        self.initial['shopName'] = self.instance.shop.name

    class Meta:
        model = Order
        exclude = ('consumer', 'shop', 'state')


class CommodityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommodityForm, self).__init__(*args, **kwargs)
        self.fields['grade'].widget.attrs['readonly'] = True
        self.fields['gradedBy'].widget.attrs['readonly'] = True

    class Meta:
        model = Commodity
        exclude = ('shop',)
