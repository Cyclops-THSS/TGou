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
from .views_auth import group_required


@group_required('Consumer')
def view_order(request):
    pass


@login_required
def view_order_id(request, id):
    pass


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
