#!/usr/bin/env python
# coding=utf-8

from django import forms
from django.forms import widgets

from goods.models import goods
from category.models import category

class GoodsForm(forms.ModelForm):

    def save(self, author, category_id, **kwargs):
        form = super(GoodsForm, self).save(commit=False, **kwargs)
        form.author = author
        selected_category = category.objects.get(id=category_id)
        selected_category.production = selected_category.production + 1
        selected_category.save()
        form.save()

    class Meta:
        model = goods
        fields = ('title', 'description', 'goods_cover', 'price')


