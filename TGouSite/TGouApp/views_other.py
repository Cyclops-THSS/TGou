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
from datetime import datetime


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
@check_request(lambda r: r.method == 'POST' and r.POST.cid and r.POST.sid and r.POST.direction and r.POST.grade, 'bad request' and Consumer.objects.get(pk=r.POST.cid) and Shop.objects.get(pk=r.POST.sid))
def apply_grading(request):
    def update(obj, g):
        tot = obj.grade * obj.gradedBy + g
        tot /= obj.gradedBy + 1
        obj.update({'grade': tot, 'gradedBy': obj.gradedBy + 1})
    consumer = Consumer.objects.get(pk=request.POST.cid)
    shop = Shop.objects.get(pk=request.POST.sid)
    direction = request.POST.direction
    time = datetime.now()
    grade = request.POST.grade
    o = Grading.objects.update_or_create(consumer=consumer, shop=shop,
                                         direction=direction, defaults={'time': time, 'grade': grade})
    update(consumer if direction else shop, grade)
