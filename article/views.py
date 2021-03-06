from django.shortcuts import render,redirect,get_object_or_404
from .models import ArticlePost,ArticleColumn
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator
from comment.models import Comment
from comment.forms import CommentForm
import markdown
from django.views import generic
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import re
from PIL import Image
from urllib.request import urlopen
from django.conf import settings

# Create your views here.

def column(request,pk):
    col = get_object_or_404(ArticleColumn,pk=pk)
    article_list = ArticlePost.objects.filter(column=col)
    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    comments = Comment.objects.all()
    return render(request,'article/index.html',context={'articles':articles,'comments':comments})

def archive(request,year,month):
    articles= ArticlePost.objects.filter(created__year=year,
                                                  created__month=month
                                                  )

    return  render(request,'article/index.html',context={'articles':articles})


def index_view(request):
    article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    comments = Comment.objects.all()
    return render(request,'article/index.html',{'articles':articles,'comments':comments})  # 返回给index用于显示

def article_list(request):

    article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list,5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles':articles}
    return render(request,'article/list.html',context)



def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    md=markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    article.body = md.convert(article.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    article.toc = m.group(1) if m is not None else ''
    article.total_views += 1
    article.save(update_fields=['total_views'])
    comment_form = CommentForm()
    context = {'article':article,'comments':comments,'comment_form':comment_form,'toc':md.toc}

    return render(request,'article/detail.html',context)

@permission_required('article.can_add_article_post')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        if article_post_form.is_valid():
            new_article=article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse("请重新填写")
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form':article_post_form}
        return render(request,'article/create.html',context)

@permission_required('article.can_delete_article_post')
def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    article.delete()
    return redirect("article:article_list")

@permission_required('article.can_change_article_post')
def article_update(request, id):


    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
