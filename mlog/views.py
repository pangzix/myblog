from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import MlogPost,MyVlogPost
from .forms import MlogPostForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator


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

def vlog_list(request):
    vlog_list = MyVlogPost.objects.all()
    paginator = Paginator(vlog_list, 5)
    page = request.GET.get('page')
    vlogs = paginator.get_page(page)
    context = {'vlogs':vlogs}
    return render(request, 'mlog/vlog.html', context)

def vlog_detail(request,pk):
    vlog = get_object_or_404(MyVlogPost,pk=pk)
    context = {'vlog':vlog}
    return render(request,'mlog/vlog_detail.html',context)