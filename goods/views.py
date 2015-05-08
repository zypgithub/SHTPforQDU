# -*- coding: utf-8 -*-

from base64 import b64encode
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db import IntegrityError
from django.forms.models import modelformset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.utils import simplejson

from category.models import category
from goods.models import goods, photo
from goods.form import GoodsForm,PhotoForm
from users.models import UserProfile

from django.db.models import Q
#todo: 关键词搜索
def list_goods(request, filter_category):
    categories = category.objects.values('name', 'production_count', 'id')
    if 'search' in request.GET:
        search_word = request.GET['search']
        print(search_word)

    try:
       nickname = UserProfile.objects.get(school_id=request.user.username).nickname
    except UserProfile.DoesNotExist:
        nickname = None
    if 'search' in request.GET:
        search_keyword = request.GET['search']
    else:
        search_keyword = ''
    qset = search_keyword.split(' ')
    query = Q()
    for keyword in qset:
        query = query & Q(title__contains=keyword)

    if filter_category == "0" or filter_category == '':#如果列表模式为0,则表示列出所有物品
        if 'order' in request.GET:
            order = request.GET['order']
            try:
                if search_keyword != '':
                    selected_goods = goods.objects.filter(query).order_by(order)
                else:
                    selected_goods = goods.objects.all().order_by(order)
            except FieldError:
                return  HttpResponse('404')
        else: 
            selected_goods = goods.objects.all().order_by('-created_at')
            order='-created_at'
       
    else:
        try:
            selected_category = category.objects.get(id=filter_category)
        except category.DoesNotExist:
           return  HttpResponse('404')
        if 'order' in request.GET:
            order = request.GET['order']
            try:
                if search_keyword != '':
                    query = query & Q(category=selected_category)
                    selected_goods = goods.objects.filter(query).order_by(order)
                else:
                    selected_goods = goods.objects.filter(category=selected_category).order_by(order)
            except FieldError:
                return  HttpResponse('404')
        else: 
            selected_goods = goods.objects.filter(category=selected_category).order_by('-created_at')
            order = '-created_at'
            
    return render(request, 'goods/goods_list.html', {'nickname': nickname, 'categories': categories, 'goods': selected_goods, 'order': order, 'category': filter_category, 'search_keyword': search_keyword})

            

def get_image(request, image_name):
    try:
        image = open('/Image/'+ image_name).read()
    except IOError:
        print(image_name)
    print(image_name)
    return HttpResponse(image)

@login_required(login_url="/users/")
def create_goods(request):
    categories = category.objects.values('name', 'production_count', 'id')
    try:
       userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        userprofile = None 
    if request.method == "GET":
        return render(request, 'goods/create_goods.html', {'userprofile': userprofile, 'categories': categories, })
    else:
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            g = form.save(request.user, request.POST['category'])
            photos = []
            for i in range(1, 5):
                photos.append(PhotoForm(request.POST, request.FILES, prefix=i))
                if photos[i - 1].is_valid():
                    photos[i - 1].save(g)
            myjson={"status": "success"}
            return HttpResponse(simplejson.dumps(myjson))
        else:
            myjson={"status": "fail"}
            return HttpResponse(simplejson.dumps(myjson))
        

def goods_details(request, goods_id):
    categories = category.objects.values('name', 'production_count', 'id')
    try:
        selected_goods = goods.objects.get(id=goods_id)
    except goods.DoesNotExist:
        return render(request, "404.html")
    selected_photos = photo.objects.filter(goods=selected_goods)
    if request.user.is_authenticated():
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return render(request, "404.html")
    else:
        selected_goods.contact = None
        selected_goods.author = User()
        userprofile = UserProfile()
    if request.user == selected_goods.author:
        is_myself = True
    else:
        is_myself = False
    return render(request, 'goods/goods_details.html', {"goods": selected_goods, "photos": selected_photos, "categories": categories, "userprofile": userprofile, "is_myself": is_myself})

@login_required(login_url="/users/")
def delete_goods(request, goods_id):
    try:
        selected_goods = goods.objects.get(id=goods_id)
    except goods.DoesNotExist:
        response = {'error_code': '110', 'status': 'fail'}
        return HttpResponse(json.dumps(response))
    if selected_goods.author != request.user:
        response = {'error_code': '111', 'status': 'fail'}
        return HttpResponse(json.dumps(response))
    selected_goods.delete()
    response = {'status': 'success'}
    return HttpResponse(json.dumps(response))

@login_required(login_url="/users/")
def modify_goods(request, goods_id):
    categories = category.objects.values('name', 'production_count', 'id')
    try:
        selected_goods = goods.objects.get(id=goods_id)
    except goods.DoesNotExist:
        return render(request, '404.html')
    if selected_goods.author != request.user:
        return render(request, '404.html')
    if request.method == "GET":
        return render(request, 'goods/modify_goods.html', { 'categories':categories, 'goods': selected_goods })
    else:
        psss
