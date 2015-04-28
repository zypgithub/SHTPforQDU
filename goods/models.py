#coding:utf-8
from django.db import models
from category.models import category
from django.contrib.auth.models import User

class goods(models.Model):
    category = models.ForeignKey(category)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=10000)
    author = models.ForeignKey(User) 
    created_at = models.DateTimeField(auto_now_add=True)
    browse_count = models.IntegerField()
    alter_at = models.DateTimeField(auto_now=True)
    
