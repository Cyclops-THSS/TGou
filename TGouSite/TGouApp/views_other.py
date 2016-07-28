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
from django.utils.translation import ugettext_lazy as _


@group_required('Consumer')
@check_request(lambda r: r.method == 'POST' and r.POST.oiid and OrderItem.objects.get(pk=r.POST.oiid), _('bad request'))
def new_comment(request):
    oi = OrderItem.objects.get(pk=r.POST.oiid)
    oc = Comment(commodity=oi.cmd, grade=5.00, message='', time=datetime.now())
    oc.save()
    return redirect('edit_comment', id=oc.id)


@group_required('Consumer')
@render_to('vEditForm.html')
def edit_comment(request, id):
    try:
        dat = Comment.objects.get(pk=id)
    except:
        raise Http404
    if dat.consumer != request.user.ConsumerProf:
        raise PermissionDenied
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=dat)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm(instance=dat)
    return {'form': form, 'entityType': 'Order'}


@group_required('Consumer')
def delete_comment(request, id):
    try:
        dat = Comment.objects.get(pk=id)
    except:
        raise Http404
    dat.delete()
    return redirect('index')


@login_required
@check_request(lambda r: r.method == 'POST' and r.POST.cid and r.POST.sid and r.POST.direction and r.POST.grade and Consumer.objects.get(pk=r.POST.cid) and Shop.objects.get(pk=r.POST.sid), _('bad request'))
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
