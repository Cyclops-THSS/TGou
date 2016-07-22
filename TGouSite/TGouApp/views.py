from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Consumer, ShopKeeper
from .forms import *
from registration.signals import *
from django.dispatch import receiver

@receiver(user_registered)
def save_profile(sender, user, request, **kwargs):
    form = UserRegForm(request.POST)
    d = ShopKeeper(user=user) if request.POST.get('type', False) == 'on' else Consumer(user=user)
    d.save()
