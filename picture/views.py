from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import PicturePost
import markdown
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
# 引入分页模块
from django.core.paginator import Paginator

# Create your views here.
def picture_list(request):
    picture_list=PicturePost.objects.all()
    context = {'pictures': picture_list}
    return render(request, 'picture/list.html', context)


def picture_detail(request, id):
    # 取出相应的文章
    # article = ArticlePost.objects.get(id=id)
    # logger.warning('Something went wrong!')
    picture = get_object_or_404(PicturePost, id=id)


    context = {
        'picture': picture,
    }
    # 载入模板，并返回context对象
    return render(request, 'picture/detail.html', context)

