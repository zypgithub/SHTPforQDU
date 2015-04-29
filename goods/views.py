# -*- coding: utf-8 -*-

from base64 import b64encode
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from category.models import category
from goods.models import goods
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

            

            
