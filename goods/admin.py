#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from goods.models import goods, photo

admin.site.register(goods)
admin.site.register(photo)
