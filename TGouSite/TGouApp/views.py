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
        return 'view_profile'


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


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
def view_profile(request):
    form = ConsumerProf(instance=request.user.ConsumerProf) if request.user.groups.filter(
        name='Consumer').exists() else ShopKeeperProf(instance=request.user.ShopKeeperProf)
    context = {
        'form': form
    }
    return HttpResponse(loader.get_template('profile/profile.html').render(context, request))


@login_required
def edit_profile(request):
    form = ConsumerProf(request.POST, instance=request.user.ConsumerProf) if request.user.groups.filter(
        name='Consumer').exists() else ShopKeeperProf(request.POST, instance=request.user.ShopKeeperProf)
    if form.is_valid():
        form.save()
    return redirect('view_profile')


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


def new_shop(request):
    pass


def edit_shop(request):
    pass


def delete_shop(request):
    pass


def save_shop(request):
    pass


def view_shop_orders(request):
    pass


def search_shop(request):
    print(request.GET.get('q', ''))
    return redirect('index')


def edit_cart(request):
    pass


def clear_cart(request):
    pass


def view_order(request):
    pass


def view_order_id(request, id):
    pass


def new_order(request):
    pass


def edit_order(request, id):
    pass


def confirm_order(request, id):
    pass


def delete_order(request, id):
    pass


def view_product(request):
    pass


def search_product(request):
    pass


def view_product_id(request, id):
    pass


def view_product_name(request, name):
    pass


def edit_product(request, id):
    pass


def delete_product(request, id):
    pass


def new_comment(request):
    pass


def edit_comment(request, id):
    pass


def delete_comment(request, id):
    pass


def apply_grading(request):
    pass


def error(request):
    pass
