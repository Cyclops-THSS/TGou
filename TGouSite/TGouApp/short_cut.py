from django.http import HttpResponse
from django.shortcuts import *
from django.conf import settings
from django.contrib.auth.decorators import *
from functools import wraps


def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render(request, output[1], output[0])
            elif isinstance(output, dict):
                return render(request, template, output)
            return output
        return wrapper
    return renderer


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


@render_to('error.html')
def error(request, message=None):
    if not message:
        message = request.session.get('msg', None)
        if message:
            del request.session['msg']
    if not message:
        raise Http404
    return {'message': message}


def check_request(_lambda, message):
    def outer(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            ret = _lambda(request)
            if ret != False and ret != None and not isinstance(ret, six.string_types):
                return func(request, *args, **kwargs)
            else:
                return error(request, message if ret == False or not isinstance(ret, six.string_types) else ret)
        return inner
    return outer
