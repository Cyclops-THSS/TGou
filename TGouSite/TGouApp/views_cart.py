from django.shortcuts import *
from django.http import HttpResponse
from django.template import loader
from .models import *
from .forms import *
from registration.signals import *
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import *
from registration.backends.simple.views import RegistrationView
from .short_cut import *
import json


@group_required('Consumer')
@render_to('cart/vCart.html')
def edit_cart(request):
    if request.method == 'POST':
        print('.')
        print(request.POST.get('cartJson'))
        print('.')
        cartJson = json.load(request.POST.get('cartJson'))
        whatamidoing = request.POST.get('whatamidoing')
        if whatamidoing == 'save':
            request.user.ConsumerProf.cart.cartitem_set.clear()
            print(request.user.ConsumerProf.cart.cartitem_set.all())
            for k, v in cartJson.items():
                _add_to_cart(k, v[0], request.user.ConsumerProf.cart)
    else:
        cartJson = {}
        for value in request.user.ConsumerProf.cart.cartitem_set.all():
            cartJson[value.commodity.id] = [value.quantity, str(value.commodity.price)]
    print(cartJson)
    return {'cart': request.user.ConsumerProf.cart, 'cartJson': json.dumps(cartJson)}


@group_required('Consumer')
def add_to_cart(request):
    _add_to_cart(Commodity.objects.get(pk=request.POST['commodityId']), request.POST['quantity'], request.user.ConsumerProf.cart)
    return redirect('edit_cart')

def _add_to_cart(commodity, quantity, cart):
    ci = CartItem(commodity=commodity, quantity=quantity, cart=cart)
    ci.save()
