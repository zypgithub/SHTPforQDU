# -*- coding: utf-8 -*-

from base64 import b64encode
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from category.models import category
from users.models import UserProfile

#to do: login check
def list_goods(requrest, filter_category, key_word):
    categories = category.objects.values('name', 'production_count')
    key_word_search = key_word.encode()
    if key_word_search == '':
        if filter_category == "all":#如果列表模式为0,则表示列出所有物品
            try:
                nickname = UserProfile.objects.get(school_id=requrest.user.username).nickname
            except UserProfile.DoesNotExist:
                return render(requrest, 'goods/dashboard.html', {'categories': categories})
            return render(requrest, 'goods/dashboard.html', {'nickname': nickname, 'cagetories': categories})
#        else if filter_category in cagetories.names():

            
