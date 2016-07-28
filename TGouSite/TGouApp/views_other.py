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
import decimal


@group_required('Consumer')
@check_request(lambda r: r.method == 'POST' and r.POST.get('oiid', None) and OrderItem.objects.get(pk=r.POST.get('oiid')), _('bad request'))
def new_comment(request):
    oi = OrderItem.objects.get(pk=request.POST.get('oiid'))
    try:
        cmt = Comment.objects.get(
            commodity=oi.cmd, consumer=request.user.ConsumerProf)
        return redirect('edit_comment', id=cmt.id)
    except:
        oc = Comment(commodity=oi.cmd, grade=5.00, message='',
                     time=datetime.now(), consumer=request.user.ConsumerProf)
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
    form = CommentForm(request.POST, instance=dat,
                       initial={'time': datetime.now()})
    if form.is_valid():
        form.save()
        return redirect('view_product_id', id=dat.commodity.id)
    return {'form': form, 'entityType': 'Comment'}


@group_required('Consumer')
def delete_comment(request, id):
    try:
        dat = Comment.objects.get(pk=id)
    except:
        raise Http404
    dat.delete()
    return redirect('index')


@login_required
@check_request(lambda r: r.method == 'POST' and r.POST.get('cid', None) and r.POST.get('sid', None) and r.POST.get('direction', None) and r.POST.get('odid', None) and r.POST.get('grade', None) and Shop.objects.get(pk=r.POST['sid']) and Consumer.objects.get(pk=r.POST['cid']), _('bad request'))
def apply_grading(request):
    def update(obj, filter, g):
        tot = obj.grade * obj.gradedBy + g
        tot /= obj.gradedBy + 1
        filter.update(grade=tot, gradedBy=obj.gradedBy + 1)
    consumer = Consumer.objects.get(pk=request.POST['cid'])
    shop = Shop.objects.get(pk=request.POST['sid'])
    direction = request.POST['direction']
    time = datetime.now()
    grade = request.POST['grade']
    o = Grading.objects.update_or_create(consumer=consumer, shop=shop,
                                         direction=direction, defaults={'time': time, 'grade': grade})
    update(consumer if direction else shop, Consumer.objects.filter(pk=consumer.id)
           if direction else Shop.objects.filter(pk=shop.id), decimal.Decimal(grade))
    return redirect('view_order_id', id=request.POST['odid'])
