from django.shortcuts import redirect
from utils import restful
from functools import wraps
from django.http import Http404


def xfz_login_require(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauthorized(message='请先登录！')
            else:
                return redirect('index')
    return wrapper


def xfz_admin_required(func):
    # @wraps 用于保存原函数的属性
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper
