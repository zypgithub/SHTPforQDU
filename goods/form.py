#!/usr/bin/env python
# coding=utf-8

from django import forms
from django.forms import widgets
from django.forms.models import BaseModelFormSet

from django.db import models
from goods.models import goods, photo
from category.models import category

class GoodsForm(forms.ModelForm):

    def save(self, user, category_id, **kwargs):
        form = super(GoodsForm, self).save(commit=False, **kwargs)
        form.author = user
        selected_category = category.objects.get(id=category_id)
        form.category = selected_category
        form.save()
        selected_category.production_count = selected_category.production_count + 1
        selected_category.save()
        return form

    class Meta:
        model = goods
        fields = ('title', 'description', 'goods_cover', 'price', 'contact')

class PhotoForm(forms.ModelForm):

    def save(self, goods, **kwargs):
        form = super(PhotoForm, self).save(commit=False, **kwargs)
        form.goods = goods
        form.save()

    class Meta:
        model = photo
        fields = ['photo',]

