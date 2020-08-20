from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .form import LoginForms, RegisterForm
from .models import User
from django.http import HttpResponse
from utils import restful
from utils.captcha.xfzcaptcha import ImgCaptcha
from io import BytesIO
from django.core.cache import cache



@require_POST
def login_view(request):
    form = LoginForms(request.POST)
    # print(form.get_error())
    if form.is_valid():
        cleaned_data = form.cleaned_data
        telephone = cleaned_data.get('telephone')
        password = cleaned_data.get('password')
        remember = cleaned_data.get('remember')
        user = authenticate(request, telephone=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(300)
                else:
                    request.session.set_expiry(0)

                    return restful.ok(message='')
            else:
                return restful.unauthorized(message='用户被冻结')
        else:
            return restful.parameter_error(message='手机号或密码错误')
    else:
        return restful.parameter_error(message=form.get_error())


def logout_view(request):
    logout(request)
    return redirect('index')


def img_captcha(request):
    img, text = ImgCaptcha.art_board()
    file = BytesIO()

    # save img to file string at Memory
    img.save(file, 'jpeg')

    # move seek to start
    file.seek(0)

    # write file to response Object
    response = HttpResponse(content_type='jpeg')
    response.write(file.read())

    response['Content_length'] = file.tell()
    text = ''.join(text)
    cache.set('img_captcha', text.lower(), 5*60)
    return response


def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password1')
        username = form.cleaned_data.get('username')

        user = User.objects.create_user(telephone=telephone,
                                        password=password,
                                        username=username)
        login(request, user)
        return restful.ok()

    else:
        return restful.parameter_error(message=form.get_error())


# def addgroup(request):
#     superuser = User.objects.get(username='admin')
#     editgroup = Group.objects.get(name='编辑')
#     superuser.groups.add(editgroup)
#     superuser.save()
#     return HttpResponse('ok')



# def index(request):
#     user = User.objects.get(username='ccc')
#     user.delete()
#     return HttpResponse('ok')


# def index(request):
#     User.objects.create_user(telephone=13055558888, username='bbb', raw_password='111111')
#     return HttpResponse('success')
