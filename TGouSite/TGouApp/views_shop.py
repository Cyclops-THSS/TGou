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


def view_shop(request):
    pass


def _view_shop(request, shop):
    category = shop.category
    categoryList = [category]
    context = {
        'categoryList': categoryList,
        'shop': shop
    }
    return render(request, 'shop/vShop.html', context)


def view_shop_id(request, id):
    shop = Shop.objects.get(pk=id)
    return _view_shop(request, shop)


def view_shop_name(request, name):
    shop = Shop.objects.get(name=name)
    return _view_shop(request, shop)


@group_required('ShopKeeper')
def new_shop(request):
    pass


@group_required('ShopKeeper')
def edit_shop(request):
    pass


@group_required('ShopKeeper')
def delete_shop(request):
    pass


def search_shop(request):
    q = request.GET.get('q')
    if request.method == 'POST':
        q = request.POST.get('q')
    cset = Shop.objects.filter(
        name__icontains=q) if q else Shop.objects.all()
    return render(request, 'shop/vShops.html', {'shops': cset, 'query': q if q else ''})
