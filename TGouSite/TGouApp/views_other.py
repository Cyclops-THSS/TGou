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
def new_comment(request):
    pass


@group_required('Consumer')
def edit_comment(request, id):
    pass


@group_required('Consumer')
def delete_comment(request, id):
    pass


@login_required
def apply_grading(request):
    pass


def error(request, message):
    pass
