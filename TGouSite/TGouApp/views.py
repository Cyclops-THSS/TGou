from django.shortcuts import *
from django.http import HttpResponse
from django.template import loader
from .models import Consumer, ShopKeeper
from .forms import *
from registration.signals import *
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import *
from registration.backends.simple.views import RegistrationView

class TRegistrationView(RegistrationView):
    form_class=UserRegForm
    def get_success_url(self, user):
        return 'view_profile'

@receiver(user_registered)
def save_profile(sender, user, request, **kwargs):
    form = UserRegForm(request.POST)
    isSK = request.POST.get('type', False) == 'on'
    d = ShopKeeper(user=user) if isSK else Consumer(user=user)
    g, create = Group.objects.get_or_create(name='ShopKeeper' if isSK else 'Consumer')
    g.user_set.add(user)
    d.save()

@login_required
def view_profile(request):
    form = ConsumerProf(instance=request.user.ConsumerProf) if request.user.groups.filter(name='Consumer').exists() else ShopKeeperProf(instance=request.user.ShopKeeperProf)
    context = {
        'form': form
    }
    return HttpResponse(loader.get_template('profile/profile.html').render(context, request))

@login_required
def edit_profile(request):
    form = ConsumerProf(request.POST, instance=request.user.ConsumerProf) if request.user.groups.filter(name='Consumer').exists() else ShopKeeperProf(request.POST, instance=request.user.ShopKeeperProf)
    if form.is_valid():
        form.save()
    return redirect('view_profile')
