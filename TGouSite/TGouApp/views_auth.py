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
from .short_cut import *


class TRegistrationView(RegistrationView):
    form_class = UserRegForm

    def get_success_url(self, user):
        return 'edit_profile'


@receiver(user_registered)
def create_profile(sender, user, request, **kwargs):
    isSK = request.POST.get('type') == 'True'
    d = ShopKeeper(user=user) if isSK else Consumer(user=user)
    g, create = Group.objects.get_or_create(
        name='ShopKeeper' if isSK else 'Consumer')
    g.user_set.add(d.user)
    d.save()
    if not isSK:
        cart = Cart(consumer=d)
        cart.save()


@login_required
@render_to('profile/profile_edit.html')
def edit_profile(request):
    if request.method == 'GET':
        form = ConsumerProf(instance=request.user.ConsumerProf) if belongTo(
            request.user, 'Consumer') else ShopKeeperProf(instance=request.user.ShopKeeperProf)
    else:
        form = ConsumerProf(request.POST, instance=request.user.ConsumerProf) if belongTo(
            request.user, 'Consumer') else ShopKeeperProf(request.POST, instance=request.user.ShopKeeperProf)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    return {'form': form}


@login_required
@render_to('profile/profile_show.html')
def view_profile(request):
    isCons = belongTo(request.user, 'Consumer')
    return {'isConsumer': isCons, 'prof': request.user.ConsumerProf if isCons else request.user.ShopKeeperProf}
