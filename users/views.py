#coding:utf-8
from base64 import b64encode
import json

from django.contrib.auth.models import User
from django.db import IntegrityError
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
        password = request.POST.get("password")
        print school_id + jw_password + " " + captcha + password
        user_info = get_user_info(request, school_id, jw_password, captcha)
        status = user_info[-1]
        if status[0] == 200:
            #TODO:捕获异常
            try:
                user = User(username=school_id)
                user.set_password(password)
                user.save()
            except IntegrityError:
                response = {'status_code': 606,
                            'error_info': '用户已存在'
                           }
                return HttpResponse(json.dumps(response))
            return render(request, 'users/user_info.html', {'user_info': user_info})
        else:
        #TODO: 错误状态的响应
            response = {'status_code': status[0],
                        'error_info' : status[1]
                       }
            #return HttpResponse(json.dumps(response))
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

