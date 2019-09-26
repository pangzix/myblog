from django.shortcuts import render,get_object_or_404,redirect
from  django.contrib.auth.decorators import login_required
from  django.http import  HttpResponse

from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment


# Create your views here.
@login_required(login_url='userprofile/login/')
def post_comment(request,article_id,parent_comment_id=None):
    article = get_object_or_404(ArticlePost,id=article_id)


    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user =request.user

            #二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("请重新输入")

    elif request.method == 'GET':
        comment_form =CommentForm()

        context = {
            'comment_form':comment_form,
            'article_id':article_id,
            'parent_comment_id':parent_comment_id
        }

        return render(request,'comment/reply.html',context)

    else:
        return HttpResponse("请重新输入")

