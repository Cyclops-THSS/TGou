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
from .views_other import error
from datetime import datetime
from .short_cut import *
from django.utils.translation import ugettext_lazy as _


@render_to('shop/vShop.html')
def _view_shop(request, shop):
    category = shop.category
    categoryList = [category]
    return {
        'categoryList': categoryList,
        'shop': shop
    }


def view_shop_id(request, id):
    try:
        shop = Shop.objects.get(pk=id)
    except:
        raise Http404
    return _view_shop(request, shop)


def view_shop_name(request, name):
    try:
        shop = Shop.objects.get(pk=id)
    except:
        raise Http404
    return _view_shop(request, shop)


@group_required('ShopKeeper')
@check_request(lambda r: not r.user.ShopKeeperProf.shop, _('You\'ve opened a shop'))
def new_shop(request):
    shop = Shop(createDate=datetime.now())
    shop.save()
    request.user.ShopKeeperProf.shop = shop
    request.user.ShopKeeperProf.save()
    return redirect('edit_shop')


@group_required('ShopKeeper')
@render_to('vEditForm.html')
def edit_shop(request):
    if request.method == 'GET':
        form = ShopForm(instance=request.user.ShopKeeperProf.shop)
    else:
        form = ShopForm(
            request.POST, instance=request.user.ShopKeeperProf.shop)
        if form.is_valid():
            form.save()
            return redirect('view_shop_id', id=request.user.ShopKeeperProf.shop.id)
    return {'form': form, 'entityType': 'shop'}


@group_required('ShopKeeper')
@check_request(lambda r: r.user.ShopKeeperProf.shop, _('You must open a shop first!'))
def delete_shop(request):
    request.user.ShopKeeperProf.shop.delete()
    request.user.ShopKeeperProf.shop = None
    request.user.ShopKeeperProf.save()
    return redirect('index')


@render_to('shop/vShops.html')
def search_shop(request):
    q = request.GET.get('q')
    if request.method == 'POST':
        q = request.POST.get('q')
    cset = Shop.objects.filter(
        name__icontains=q) if q else Shop.objects.all()
    return {'shops': cset, 'query': q if q else ''}

@render_to('shop/vShopCategory.html')
def view_shop_in_category(request):
    q = request.GET.get('q')
    if request.method == 'POST':
        q = request.POST.get('q')
    cset = Shop.objects.filter(
        category=q) if q else Shop.objects.all()
    categoryName = ShopCategory.objects.filter(id=q)[0].name if q else ""
    return {'shops': cset, 'categoryName': categoryName}

@render_to('shop/vShopCategories.html')
def view_shop_categories(request):
    return {'set': ShopCategory.objects.all()}
