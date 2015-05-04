# -*- coding: utf-8 -*-

from base64 import b64encode
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.utils import simplejson

from category.models import category
from goods.models import goods, photo
from goods.form import GoodsForm, PhotoForm
from users.models import UserProfile

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
    if filter_category == "0":#如果列表模式为0,则表示列出所有物品
        selected_goods = goods.objects.all()
    else:
        try:
            selected_category = category.objects.get(id=filter_category)
            selected_goods = goods.objects.filter(category=selected_category)
        except goods.DoesNotExist:
            selected_goods = []
        except category.DoesNotExist:
           return  HttpResponse('404')
    return render(request, 'goods/goods_list.html', {'nickname': nickname, 'categories': categories, 'goods': selected_goods})

            

def get_image(request, image_name):
    try:
        image = open('/Image/'+ image_name).read()
    except IOError:
        print(image_name)
    print(image_name)
    return HttpResponse(image)

@login_required(login_url="/users/")
def create_goods(request):
    '''
    if request.method == "POST":
       form = createGoodsForm(request.POST)
       if form.is_valid()
    else:
        return render(request, '',)
        '''
    categories = category.objects.values('name', 'production_count', 'id')
    try:
       nickname = UserProfile.objects.get(school_id=request.user.username).nickname
    except UserProfile.DoesNotExist:
        nickname = None 
    if request.method == "GET":
        return render(request, 'goods/create_goods.html', {'nickname': nickname, 'categories': categories})
    else:
        form = GoodsForm(request.POST, request.FILES)
      #  photoform = PhotoForm(request.POST, request.FILES)
        #if photoform.is_valid():
        if form.is_valid():
            form.save(request.user, request.POST['category'])
            myjson={"status": "success"}
            return HttpResponse(simplejson.dumps(myjson))
        else:
            myjson={"status": "fail"}
            return HttpResponse(simplejson.dumps(myjson))
        

def goods_details(request, goods_id):
    try:
        selected_goods = goods.objects.get(id=goods_id)
    except goods.DoesNotExist:
        return render(request, "404.html")
    selected_photos = photo.objects.filter(goods=selected_goods)
    if not request.user.is_authenticated():
        selected_goods.contact = None
        selected_goods.author = User()
    return render(request, 'goods/goods_details.html', {"goods": selected_goods, "photos":selected_photos})
