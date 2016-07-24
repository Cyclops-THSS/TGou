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


@group_required('ShopKeeper')
def new_product(request):
    pass


def view_product(request):
    pass


def search_product(request):
    pass


def view_product_id(request, id):
    prod = Commodity.objects.get(pk=id)
    comments = prod.comment_set.all()
    context = {
        'commodity': prod,
        'categoryList': [prod.category],
        'comments': comments,
        'average': prod.grade
    }
    return render(request, 'product/vCommodity.html', context)


@group_required('ShopKeeper')
def edit_product(request, id):
    pass


@group_required('ShopKeeper')
def delete_product(request, id):
    pass
