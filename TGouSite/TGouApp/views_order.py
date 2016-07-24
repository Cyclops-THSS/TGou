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
from .views_auth import group_required, belongTo
from datetime import datetime

@login_required
def view_order(request):
    isConsumer = belongTo(request.user, 'Consumer')
    after = request.GET.get('after')
    before = request.GET.get('before')
    left = datetime.min
    right = datetime.max
    if after:
        y, m, d = after.split('-')
        left = datetime(int(y), int(m), int(d))
    if before:
        y, m, d = before.split('-')
        right = datetime(int(y), int(m), int(d))
    oset = Order.objects.filter(time__range=[left,right])
    return render(request, 'order/vOrders.html', {'orders': oset, 'isConsumer': isConsumer})


@login_required
def view_order_id(request, id):
    order = Order.objects.get(pk=id)
    return render(request, 'order/vOrder.html', {'order': order})


@group_required('Consumer')
def new_order(request):
    pass


@login_required
def edit_order(request, id):
    pass


@group_required('Consumer')
def confirm_order(request, id):
    pass


@login_required
def delete_order(request, id):
    pass
