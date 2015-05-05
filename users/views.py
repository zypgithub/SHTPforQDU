#coding:utf-8

from base64 import b64encode
import json

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


#@login_required(login_url='student_index')
#@is_student()
def user_logout(request):
    logout(request)
    return redirect('user_index')

#@login_required()
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
            return HttpResponseRedirect('/users/modify/12345/')
           # return HttpResponse(simplejson.dumps(response))
        else:
            #TODO: form error tip
            response = {"status": "fail"}
            return HttpResponse(simplejson.dumps(response))
    else:
        return render(request, 'users/user_profile.html',{'UserProfileForm': user})

#@login_required()
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
            return HttpResponseRedirect('/users/profile/12345/')
           # return HttpResponse(simplejson.dumps(response))
        else:
            #TODO: form error tip
            response = {"status": "fail"}
            return HttpResponse(simplejson.dumps(response))
    else:
<<<<<<< HEAD
        return render(request, 'users/user_modify.html',{'UserProfileForm': user})
=======
         return render(request, 'users/user_modify.html',{'userprofile': user})

>>>>>>> c024954cc593aa74877b1444261758ec3e27425b

#@login_required()
def changepsw(request, school_id):
    try:
        user = UserProfile.objects.get(school_id=school_id) 
    except UserProfile.DoesNotExist:
	raise Http404      
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance = user)
	if form.is_valid():  
	    user = authenticate(username=username,password=data['password'])
	    print(form.password)
	    if user is not None:
	        if form.cleaned_data['new_pwd'] == form.cleaned_data['new_psw2']:
	            user.set_password(form.cleaned_date['new_pwd'])
		    user.save()
		    return HttpResponseRedirect('/users/')
	        else:
		    response = {"status": "fail1"}#error.append('Please input the same password')
	    else:		      
		 response = {"status": "fail2"}#error.append('Please correct the old password')
	else:
	     response = {"status": "fail3"}#error.append('Please input the required domain')
             return render(request, 'users/changepsw.html', {'UserProfileForm': user})
    else:
      return render(request, 'users/changepsw.html', {'UserProfileForm': user})
    

def index(request):
    if 'next' in request.GET:
        return render(request, 'users/index.html', {'next': request.GET.get('next')})
    else:
        return render(request, 'users/index.html')
