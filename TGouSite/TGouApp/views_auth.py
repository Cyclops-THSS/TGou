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


def belongTo(user, group):
    return user.groups.filter(name=group).exists()


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
        form = ConsumerProf(instance=request.user.ConsumerProf) if belongTo(
            request.user, 'Consumer') else ShopKeeperProf(instance=request.user.ShopKeeperProf)
    else:
        form = ConsumerProf(request.POST, instance=request.user.ConsumerProf) if belongTo(
            request.user, 'Consumer') else ShopKeeperProf(request.POST, instance=request.user.ShopKeeperProf)
        if form.is_valid():
            form.save()
    return HttpResponse(loader.get_template('profile/profile.html').render({'form': form}, request))
