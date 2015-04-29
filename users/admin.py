#!/usr/bin/env python
# coding=utf-8


from django.contrib import admin
from users.models import UserProfile

admin.site.register(UserProfile)
