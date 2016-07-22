from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Consumer, ShopKeeper
from .forms import *
from registration.signals import *
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(user_registered)
def save_profile(sender, user, request, **kwargs):
    form = UserRegForm(request.POST)
    isSK = request.POST.get('type', False) == 'on'
    d = ShopKeeper(user=user) if isSK else Consumer(user=user)
    g, create = Group.objects.get_or_create(name='ShopKeeper' if isSK else 'Consumer')
    g.user_set.add(user)
    d.save()
