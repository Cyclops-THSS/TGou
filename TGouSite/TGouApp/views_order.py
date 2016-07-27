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
from datetime import datetime, timedelta
from enum import Enum, unique
from .short_cut import *


@unique
class State(Enum):
    new = 0  # never used
    paying = 1
    paid = 2
    sent = 3
    finished = 4
    returning = 5
    refunding = 6
    canceled = 7


@login_required
@render_to('order/vOrders.html')
def view_order(request):
    isConsumer = belongTo(request.user, 'Consumer')
    after = request.GET.get('after')
    before = request.GET.get('before')
    left = datetime(1910, 1, 1)  # datetime.min causes complaints here
    right = datetime.max
    if after:
        y, m, d = after.split('-')
        left = datetime(int(y), int(m), int(d))
    if before:
        y, m, d = before.split('-')
        right = datetime(int(y), int(m), int(d))
    oset = Order.objects.filter(time__range=[left, right])
    return {'orders': oset, 'isConsumer': isConsumer}


@login_required
@render_to('order/vOrder.html')
def view_order_id(request, id):
    order = Order.objects.get(pk=id)
    if belongTo(request.user, 'Consumer') and order.consumer.user != request.user:
        raise PermissionDenied
    elif order.shop.ShopKeeper.user != request.user:
        raise PermissionDenied
    return {'order': order}


@group_required('Consumer')
def new_order(request):
    order = Order(consumer=request.user.ConsumerProf, shop=request.user.ConsumerProf.cart.cartitem_set.all()[
                  0].commodity.shop, time=datetime.now())
    order.save()
    for item in request.user.ConsumerProf.cart.cartitem_set.all():
        o = OrderItem(item, order)
        order.price += float(item.quantity * item.commodity.price)
        o.save()
    order.save()
    request.user.ConsumerProf.cart.cartitem_set.clear()
    return redirect('edit_order', id=order.id)


@login_required
@render_to('vEditForm.html')
def edit_order(request, id):
    order = Order.objects.get(pk=id)
    if order.consumer.user != request.user:
        raise PermissionDenied
    if request.method == 'GET':
        form = OrderForm(instance=order)
    else:
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
    return {'form': form, 'entityType': 'Order'}


@group_required('Consumer')
def confirm_order(request, id):
    order = Order.objects.get(pk=id)
    if order.consumer.user != request.user:
        raise PermissionDenied
    order.state = State.finished
    return redirect('view_order')


@group_required('Consumer')
def delete_order(request, id):
    order = Order.objects.get(pk=id)
    if order.consumer.user != request.user:
        raise PermissionDenied
    order.delete()
    return redirect('view_order')
