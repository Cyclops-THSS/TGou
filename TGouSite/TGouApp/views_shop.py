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
from .views_other import error
from datetime import datetime


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
    if request.user.ShopKeeperProf.shop:
        return error(request, 'You\'ve opened a shop')
    shop = Shop(createDate=datetime.now())
    shop.save()
    request.user.ShopKeeperProf.shop = shop
    request.user.ShopKeeperProf.save()
    return redirect('edit_shop')


@group_required('ShopKeeper')
def edit_shop(request):
    if request.method == 'GET':
        form = ShopForm(instance=request.user.ShopKeeperProf.shop)
    else:
        form = ShopForm(
            request.POST, instance=request.user.ShopKeeperProf.shop)
        if form.is_valid():
            form.save()
    return render(request, 'vEditForm.html', {'form': form, 'entityType': 'shop'})


@group_required('ShopKeeper')
def delete_shop(request):
    request.user.ShopKeeperProf.shop.delete()
    return redirect('index')


def search_shop(request):
    q = request.GET.get('q')
    if request.method == 'POST':
        q = request.POST.get('q')
    cset = Shop.objects.filter(
        name__icontains=q) if q else Shop.objects.all()
    return render(request, 'shop/vShops.html', {'shops': cset, 'query': q if q else ''})
