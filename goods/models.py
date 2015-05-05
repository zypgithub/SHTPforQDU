#coding:utf-8
from django.db import models
from category.models import category
from django.contrib.auth.models import User


class goods(models.Model):
    category = models.ForeignKey(category)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=10000)
    author = models.ForeignKey(User) 
    created_at = models.DateTimeField(auto_now_add=True)
    browse_count = models.IntegerField(default=0)
    alter_at = models.DateTimeField(auto_now=True)
    goods_cover = models.ImageField(upload_to="../Image", default="Image/defaultPhotoNotFound", blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=100, blank=False)

    class Meta:
       verbose_name = "goods"
       verbose_name_plural = "goods"
    
    def __unicode__(self):
        return u"goods name: %s" % self.title



class photo(models.Model):
    photo = models.ImageField(upload_to="../Image")
    goods = models.ForeignKey(goods)
    upload_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "photo"
        verbose_name_plural = "photo"

    def __unicode__(self):
        return u"photo belongs to %s" % self.goods
