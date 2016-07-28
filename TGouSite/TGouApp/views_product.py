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
from django import forms
from enum import Enum, unique
from .views_other import error
from .short_cut import *
from django.utils.translation import ugettext_lazy as _


@unique
class State(Enum):
    unavailable = 1
    available = 0


@group_required('ShopKeeper')
@check_request(lambda r: r.user.ShopKeeperProf.shop, _('You must open a shop first!'))
def new_product(request):
    prod = Commodity(shop=request.user.ShopKeeperProf.shop)
    prod.save()
    return redirect('edit_product', id=prod.id)


@render_to('product/vCommodities.html')
def search_product(request):
    q = request.GET.get('q')
    if request.method == 'POST':
        q = request.POST.get('q')
    cset = Commodity.objects.filter(
        name__icontains=q) if q else Commodity.objects.all()
    return {'commodities': cset, 'query': q if q else ''}


@render_to('product/vCommodity.html')
def view_product_id(request, id):
    try:
        prod = Commodity.objects.get(pk=id)
    except:
        raise Http404
    comments = prod.comment_set.all()
    return {
        'commodity': prod,
        'categoryList': [prod.category],
        'comments': comments,
        'average': prod.grade
    }


@group_required('ShopKeeper')
@render_to('vEditForm.html')
def edit_product(request, id):
    try:
        prod = Commodity.objects.get(pk=id)
    except:
        raise Http404
    if prod.shop.ShopKeeper.user.id != request.user.id:
        raise PermissionDenied
    if request.method == 'GET':
        form = CommodityForm(instance=prod)
    else:
        form = CommodityForm(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            return redirect('view_product_id', id=id)
    return {'form': form, 'entityType': 'product'}


@group_required('ShopKeeper')
def delete_product(request, id):
    try:
        prod = Commodity.objects.get(pk=id)
    except:
        raise Http404
    if prod.shop.ShopKeeper.user.id != request.user.id:
        raise PermissionDenied
    shopid = prod.shop.id
    prod.delete()
    return redirect('view_shop_id', id=shopid)
