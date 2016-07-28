from registration.forms import RegistrationFormUniqueEmail
from django import forms
from .models import *
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from enum import Enum, unique


@unique
class OState(Enum):
    new = 0  # never used
    paying = 1
    paid = 2
    sent = 3
    finished = 4
    returning = 5
    refunding = 6
    canceled = 7


class UserRegForm(RegistrationFormUniqueEmail):
    """add check about type of registration"""
    type = forms.ChoiceField(label=_('As Shop Keeper? '), choices=((False, _('No')), (True, _('Yes'))),
                             initial=False, required=False)


class BaseUserProf(forms.ModelForm):
    email = forms.EmailField(disabled=True, label=_('Register Email'))
    username = forms.CharField(
        max_length=30, disabled=True, label=_('Login Name'))
    datejoined = forms.DateField(disabled=True, label=_('Date Registered'))

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
            'dftAddress': _('Default Address'),
            'dftPayType': _('Default Paying Method')
        }


class ShopKeeperProf(BaseUserProf):

    class Meta:
        model = ShopKeeper
        exclude = ('user', 'shop')
        labels = {
            'account': _('Shroff Account'),
        }


class ShopForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)
        self.fields['createDate'].widget.attrs['readonly'] = True
        self.fields['grade'].widget.attrs['readonly'] = True
        self.fields['gradedBy'].widget.attrs['readonly'] = True

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
        self.fields['state'] = forms.ChoiceField(label=_('state'), choices=((0, _('new')), (1, _(
            'paying')), (3, _('paid')), (4, _('sent')), (5, _('finished'))), initial=self.instance.state)

    class Meta:
        model = Order
        exclude = ('consumer', 'shop')


class CommodityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommodityForm, self).__init__(*args, **kwargs)
        self.fields['grade'].widget.attrs['readonly'] = True
        self.fields['gradedBy'].widget.attrs['readonly'] = True
        self.fields['state'] = forms.ChoiceField(label=_('state'), choices=(
            (0, _('available')), (1, _('unavailable'))), initial=0, required=True)

    class Meta:
        model = Commodity
        exclude = ('shop',)


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        exclude = ('time', 'consumer', 'commodity')
