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
from .views_other import error
import json


@group_required('Consumer')
@render_to('cart/vCart.html')
def edit_cart(request):
    def save_cart(json):
        request.user.ConsumerProf.cart.cartitem_set.clear()
        for k, v in json.items():
            _add_to_cart(Commodity.objects.get(pk=int(k)), v[
                         0], request.user.ConsumerProf.cart)
    if request.method == 'POST':
        cartJson = json.loads(request.POST.get('cartJson'))
        whatamidoing = request.POST.get('whatamidoing')
        if whatamidoing == 'save':
            save_cart(cartJson)
        elif whatamidoing == 'submit':
            save_cart(cartJson)
            return redirect('new_order')
    else:
        cartJson = {}
        for value in request.user.ConsumerProf.cart.cartitem_set.all():
            cartJson[value.commodity.id] = [
                value.quantity, str(value.commodity.price)]
    return {'cart': request.user.ConsumerProf.cart, 'cartJson': json.dumps(cartJson)}


@group_required('Consumer')
def add_to_cart(request):
    cmd = Commodity.objects.get(pk=request.POST['commodityId'])
    if request.user.ConsumerProf.cart.cartitem_set.count() > 0 and request.user.ConsumerProf.cart.cartitem_set.all()[0].commodity.shop != cmd.shop:
        return error(request, 'You must apply your cart with another store\'s products first!')
    _add_to_cart(cmd, request.POST['quantity'], request.user.ConsumerProf.cart)
    return redirect('edit_cart')


def _add_to_cart(commodity, quantity, cart):
    ci = CartItem(commodity=commodity, quantity=quantity, cart=cart)
    ci.save()
