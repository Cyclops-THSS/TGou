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
from django.utils.translation import ugettext_lazy as _


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


def check_for_add_to_cart(r):
    try:
        cmd = Commodity.objects.get(pk=r.POST['commodityId'])
    except:
        return False
    if (r.user.ConsumerProf.cart.cartitem_set.count() > 0 and r.user.ConsumerProf.cart.cartitem_set.all()[0].commodity.shop != cmd.shop):
        return _('You must apply your cart with another store\'s products first!')
    return True


@group_required('Consumer')
@check_request(check_for_add_to_cart, _('bad request'))
def add_to_cart(request):
    cmd = Commodity.objects.get(pk=request.POST['commodityId'])
    _add_to_cart(cmd, request.POST['quantity'], request.user.ConsumerProf.cart)
    return redirect('edit_cart')


def _add_to_cart(commodity, quantity, cart):
    ci = CartItem(commodity=commodity, quantity=quantity, cart=cart)
    ci.save()
