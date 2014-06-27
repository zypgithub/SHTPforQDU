#coding:utf-8
from base64 import b64encode

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from users.forms import UserProfileForm
from users.models import UserProfile
from users.utils import get_captcha
from users.utils import get_user_info


def refresh_captcha(request):
    return b64encode(get_captcha(request))

def register(request):
    if request.method == "GET":
        captcha = get_captcha(request)
        captcha = b64encode(captcha)
        return render(request, 'users/register.html', {'captcha': captcha})

    if request.method == "POST":
        school_id = request.POST.get("school_id")
        jw_password = request.POST.get("jw_password")
        captcha = request.POST.get("captcha")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        user_info = get_user_info(request, school_id, jw_password, captcha)
        status = user_info[-1]
        if status[0] == 200:
            #TODO:捕获异常
            user = User(username=school_id)
            user.set_password(password)
            user.save()
            return render(request, 'users/user_info.html', {'user_info': user_info})
        #TODO: 错误状态的响应
        return HttpResponse(status[1], content_type="text/html;charset=utf-8")

def save_user(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            school_id = form.cleaned_data['school_id']
            user = User.objects.get(username=school_id)
            form.save(user=user)
        else:
            #TODO:信息验证失败的响应
            print form.errors
            return HttpResponse("Register failed!" + form.errors, content_type="text/html")
        #TODO:注册成功的响应
        return HttpResponse("register completed!", content_type="text/html")

