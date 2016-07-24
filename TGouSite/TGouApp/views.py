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


class TRegistrationView(RegistrationView):
    form_class = UserRegForm

    def get_success_url(self, user):
        return 'edit_profile'


def group_required(group, login_url='auth_login', raise_exception=True):
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group
        if user.groups.filter(name__in=groups).exists():
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url=login_url)


@receiver(user_registered)
def create_profile(sender, user, request, **kwargs):
    form = UserRegForm(request.POST)
    isSK = request.POST.get('type', False) == 'on'
    d = ShopKeeper(user=user) if isSK else Consumer(user=user)
    g, create = Group.objects.get_or_create(
        name='ShopKeeper' if isSK else 'Consumer')
    g.user_set.add(user)
    d.save()


@login_required
def edit_profile(request):
    if request.method == 'GET':
        form = ConsumerProf(instance=request.user.ConsumerProf) if request.user.groups.filter(
            name='Consumer').exists() else ShopKeeperProf(instance=request.user.ShopKeeperProf)
    else:
        form = ConsumerProf(request.POST, instance=request.user.ConsumerProf) if request.user.groups.filter(
            name='Consumer').exists() else ShopKeeperProf(request.POST, instance=request.user.ShopKeeperProf)
        if form.is_valid():
            form.save()
    return HttpResponse(loader.get_template('profile/profile.html').render({'form': form}, request))


def view_shop(request):
    pass


def view_shop_id(request, id):
    shop = Shop.objects.get(pk=id)
    category = shop.category
    categoryList = [category]
    context = {
        'categoryList': categoryList,
        'shop': shop
    }
    return HttpResponse(loader.get_template('vShop.html').render(context, request))


def view_shop_name(request, name):
    pass


@group_required('ShopKeeper')
def new_shop(request):
    pass


@group_required('ShopKeeper')
def edit_shop(request):
    pass


@group_required('ShopKeeper')
def delete_shop(request):
    pass


@group_required('ShopKeeper')
def view_shop_orders(request):
    pass


def search_shop(request):
    pass


@group_required('Consumer')
def edit_cart(request):
    pass


@group_required('Consumer')
def clear_cart(request):
    pass


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


@group_required('ShopKeeper')
def new_product(request):
    pass


def view_product(request):
    pass


def search_product(request):
    pass


def view_product_id(request, id):
    pass


def view_product_name(request, name):
    pass


@group_required('ShopKeeper')
def edit_product(request, id):
    pass


@group_required('ShopKeeper')
def delete_product(request, id):
    pass


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
