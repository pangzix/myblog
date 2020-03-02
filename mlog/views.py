from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import MlogPost
from .forms import MlogPostForm
from django.contrib.auth.models import User


def mlog_result(request):
    mlogs = MlogPost.objects.all()

    if request.method == "POST":
        mlog_post_form = MlogPostForm(data=request.POST)
        print(MlogPostForm)
        if mlog_post_form.is_valid():
            new_mlog = mlog_post_form.save(commit=False)
            new_mlog.author = User.objects.get(id=1)
            new_mlog.save()
            return redirect("mlog:mlog_result")
        else:
            return HttpResponse("error")

    else:
        mlog_post_form = MlogPostForm()
        context = {'mlog_post_form':mlog_post_form,'mlogs':mlogs}

        return render(request,'mlog/result.html',context)

