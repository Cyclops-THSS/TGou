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
from django import forms
from enum import Enum, unique
from .views_other import error


@unique
class State(Enum):
    unavailable = 1
    available = 0


@group_required('ShopKeeper')
def new_product(request):
    if not request.user.ShopKeeperProf.shop:
        return error(request, 'You must open a shop first!')
    prod = Commodity(shop=request.user.ShopKeeperProf.shop)
    prod.save()
    return redirect('edit_product', id=prod.id)


def search_product(request):
    q = request.GET.get('q')
    if request.method == 'POST':
        q = request.POST.get('q')
    cset = Commodity.objects.filter(
        name__icontains=q) if q else Commodity.objects.all()
    return render(request, 'product/vCommodities.html', {'commodities': cset, 'query': q if q else ''})


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
    prod = Commodity.objects.get(pk=id)
    if prod.shop.ShopKeeper.user.id != request.user.id:
        raise PermissionDenied
    if request.method == 'GET':
        form = CommodityForm(instance=prod)
    else:
        form = CommodityForm(request.POST, instance=prod)
        if form.is_valid():
            form.save()
    return render(request, 'vEditForm.html', {'form': form, 'entityType': 'product'})


@group_required('ShopKeeper')
def delete_product(request, id):
    prod = Commodity.objects.get(pk=id)
    if prod.shop.ShopKeeper.user.id != request.user.id:
        raise PermissionDenied
    shopid = prod.shop.id
    prod.delete()
    return redirect('view_shop_id', id=shopid)
