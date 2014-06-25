#coding:utf-8
from base64 import b64encode

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from users.models import UserProfile
from users.utils import get_captcha
from users.utils import get_user_info


def register(request):
    if request.method == "GET":
        captcha = get_captcha(request)
        captcha = b64encode(captcha)
        return render(request, 'users/register.html', {'captcha': captcha})

    if request.method == "POST":
        school_id = request.POST.get("school_id")
        jw_password = request.POST.get("jw_password")
        captcha = request.POST.get("captcha")
        user_info = get_user_info(request, school_id, jw_password, captcha)
        status = user_info[-1]
        if status[0] == 200:
            return render(request, 'users/user_info.html', {'user_info': user_info})
        #TODO: 错误状态的响应
        return HttpResponse(status[1], content_type="text/html;charset=utf-8")

def save_user(request):
    if request.method == "POST":
        school_id = request.POST.get("school_id")
        username = request.POST.get("username")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        college = request.POST.get("college")
        grade = request.POST.get("grade")
        major = request.POST.get("major")
        gender = request.POST.get("gender")
        user = User(username=school_id)
        user.set_password(password)
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.school_id = school_id
        user_profile.nickname = nickname
        user_profile.password = password
        user_profile.college = college
        user_profile.grade = grade
        user_profile.major = major
        user_profile.gender = gender
        user_profile.save()
        #TODO:注册成功的响应
        return HttpResponse("register completed!", content_type="text/html")

