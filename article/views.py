from django.shortcuts import render,redirect
from .models import ArticlePost
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from comment.models import Comment
from comment.forms import CommentForm
import markdown
# Create your views here.


def index_view(request):
    articles = ArticlePost.objects.all()
    comments = Comment.objects.all()
    return render(request,'article/index.html',{'ariticle_list':articles,'comments':comments})  # 返回给index用于显示

def article_list(request):

    article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list,1)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles':article_list}
    return render(request,'article/list.html',context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    article.total_views += 1
    article.save(update_fields=['total_views'])
    comment_form = CommentForm()
    context = {'articles':article,'comment':comments,'comment_form':comment_form,}

    return render(request,'article/detail.html',context)

@login_required(login_url='userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
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

@login_required(login_url='/userprofile/login/')
def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    article.delete()
    return redirect("article:article_list")

@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()

            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("请重新输入")

    else:
        article_post_form =ArticlePostForm()
        context = {'article':article,'article_post_form':article_post_form}
        return render(request,'article/update.html',context)
