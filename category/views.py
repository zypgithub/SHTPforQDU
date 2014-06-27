# coding:utf-8
from category import category
from shortcuts import render

def categories_list(request):
    category_list = category.objects.all().order_by('-created_at')
    return (render(
            request,
            'category/categories_list.html',
            {'categories_list': category_list})
    )
