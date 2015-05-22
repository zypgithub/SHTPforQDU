#coding:utf-8

from base64 import b64encode
import json

from django.core import signing
from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.utils import simplejson

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
        pswquestion = request.POST.get("pswquestion")
        pswanwser = request.POST.get("pswanwser")
        user_info = get_user_info(request, school_id, jw_password, captcha)
        status = user_info[-1]
        if status[0] == 200:
            
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
      
            response = {'status_code': status[0],
                        'error_info' : status[1]
                       }
            return HttpResponse(json.dumps(response))
        return HttpResponse(status[1], content_type="text/html;charset=utf-8")

def save_user(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            school_id = form.cleaned_data['school_id']
            user = User.objects.get(username=school_id)
            form.save(user=user)
            #TODO:注册成功的响应
            return HttpResponse("register completed!", content_type="text/html")
        else:
            #TODO:信息验证失败的响应
            print form.errors
            return HttpResponse("Register failed!" + form.errors, content_type="text/html")
    else:       
        return HttpResponse("Register failed!", content_type="text/html")
   
        

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('school_id')
        password = request.POST.get('password')        
        user = authenticate(username=username, password=password)
        if isinstance(user, User):
            login(request, user)
            if request.POST.get('next') == "":
                return redirect('user_dashboard')
            else:
                return HttpResponseRedirect(request.POST.get('next'))
    return redirect('user_index')
    #TODO:登录失败（账户密码错误）的提示功能


def dashboard(request):
    userprofile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/dashboard.html', {"userprofile": userprofile})


@login_required(login_url='')
def user_logout(request):
    logout(request)
    return redirect('user_index')

@login_required()
def user_profile(request, school_id):
    try:
        user = UserProfile.objects.get(school_id=school_id)
    except UserProfile.DoesNotExist:
	raise Http404
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance = user)
        if form.is_valid():
            user.school_id = form.cleaned_data['school_id']
	    user.username = form.cleaned_data['username']
	    user.nickname = form.cleaned_data['nickname']
	    user.college = form.cleaned_data['college']
	    user.grade = form.cleaned_data['grade']
	    user.major = form.cleaned_data['major']
	    user.gender = form.cleaned_data['gender']
	    user.telephone = form.cleaned_data['telephone']
            user.qq = form.cleaned_data['qq']
            response = {"status": "ok"}
            return HttpResponseRedirect('/users/profile/(?P<school_id>\d+)/')
            return HttpResponse(simplejson.dumps(response))
        else:
            #TODO: form error tip
            response = {"status": "fail"}
            return HttpResponse(simplejson.dumps(response))
    else:
        return render(request, 'users/user_profile.html',{'UserProfileForm': user})

@login_required()
def user_modify(request, school_id):
    try:
        user = UserProfile.objects.get(school_id=school_id)
    except UserProfile.DoesNotExist:
    	raise Http404
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance = user)
        if form.is_valid():
            user.school_id = form.cleaned_data['school_id']
            user.username = form.cleaned_data['username']
            user.nickname = form.cleaned_data['nickname']
            user.college = form.cleaned_data['college']
            user.grade = form.cleaned_data['grade']
            user.major = form.cleaned_data['major']
            user.gender = form.cleaned_data['gender']
            user.telephone = form.cleaned_data['telephone']
            user.qq = form.cleaned_data['qq']
            user.save()
            response = {"status": "ok"}
            return HttpResponseRedirect('/users/profile/(?P<school_id>\d+)/')
           # return HttpResponse(simplejson.dumps(response))
        else:
            #TODO: form error tip
            response = {"status": "fail"}
            return HttpResponse(simplejson.dumps(response))
    else:
         return render(request, 'users/user_modify.html',{'userprofile': user})


@login_required()
def changepsw(request):
    if request.method == 'GET':
        print(request.user.username)
        return render(request, 'users/changepsw.html', {'username': request.user.username})           
    if request.method == 'POST':
        new_psw = request.POST.get('new_psw') 
        new_psw2 = request.POST.get('new_psw2')
        if not new_psw or not new_psw2:
           response = {"status": "tianxiemima"}
           return HttpResponse(simplejson.dumps(response)) 
        if new_psw != new_psw2:
           response = {"status": "buyiyang"}
           return HttpResponse(simplejson.dumps(response)) 
        user = User.objects.get(username=request.user.username)
        user.set_password(new_psw)
        print(new_psw)
        user.save()
    return HttpResponseRedirect('/users/profile/(?P<school_id>\d+)/') 

def retrievepsw(request):
    if request.method == 'GET':
        print(request.user.username)
        return render(request, 'users/retrievepsw.html', {'username': request.user.username})     
    if request.method == 'POST':
        username = request.POST.get('username')
        user = UserProfile.objects.get(username = username)
        form = UserProfileForm(request.POST, instance = user)
        if form.is_valid():
            user.pswquestion = form.cleaned_data['pswquestion']
            user.pswanwser = form.cleaned_data['pswanwser']
            psw = user.get_password()
            return HttpResponse("your psw is :"+psw, content_type="text/html")
    response = {"status": "fail"}
    return HttpResponse(simplejson.dumps(response)) 
    

def index(request):
    if 'next' in request.GET:
        return render(request, 'users/index.html', {'next': request.GET.get('next')})
    else:
        return render(request, 'users/index.html')
