from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User
from allauth.socialaccount.providers.github.provider import GitHubAccount
from allauth.socialaccount.models import SocialAccount
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_logout(request):
    logout(request)
    return redirect("article:article_list")



def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request,new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("请重新输入")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form':user_register_form}
        return render(request,'userprofile/register.html',context)
    else:
        return HttpResponse("请求错误")



@login_required(login_url='account_login')
def profile_edit(request,id):
    user = User.objects.get(id=id)
    if request.user == user:
        if SocialAccount.objects.filter(user_id=id).exists():
            profile_social = SocialAccount.objects.get(user_id=id)
            profile = Profile.objects.get(user_id=id)

            if request.method == 'POST':
                if request.user != user:
                    return HttpResponse("ERROR")
                profile_form = ProfileForm(request.POST, request.FILES)
                if profile_form.is_valid():
                    profile_cd = profile_form.cleaned_data
                    profile.phone = profile_cd['phone']
                    profile.bio = profile_cd['bio']
                    profile.save()
                    return redirect("userprofile:edit", id=id)
                else:
                    return HttpResponse("ERROR")
            elif request.method == 'GET':
                profile_form = ProfileForm()
                context = {'profile_form': profile_form, 'profile': profile, 'user': user,'profile_social':profile_social}
                return render(request, 'userprofile/edit_social.html', context)
            else:
                return HttpResponse("ERROR")

        else:
            profile = Profile.objects.get(user_id=id)


        if request.method == 'POST':
            if request.user !=user:
                return HttpResponse("ERROR")
            profile_form = ProfileForm(request.POST,request.FILES)
            if profile_form.is_valid():
                profile_cd = profile_form.cleaned_data
                profile.phone = profile_cd['phone']
                profile.bio = profile_cd['bio']
                if 'avatar' in request.FILES:
                    profile.avatar = profile_cd["avatar"]
                profile.save()
                return redirect("userprofile:edit",id=id)
            else:
                return HttpResponse("ERROR")
        elif request.method == 'GET':
            profile_form = ProfileForm()
            context = {'profile_form':profile_form,'profile':profile,'user':user}
            return render(request, 'userprofile/edit_local.html', context)
        else:
            return HttpResponse("ERROR")

    else:
        return HttpResponse("哦豁，崩溃了")


@login_required(login_url='account_login')
def profile_info(request,id):
    user = User.objects.get(id=id)
    if SocialAccount.objects.filter(user_id=id).exists():
        profile_social = SocialAccount.objects.get(user_id=id)
        profile = Profile.objects.get(user_id=id)
        context = {'profile': profile,'profile_socila':profile_social,'user': user}
        return render(request, 'userprofile/info_social.html', context)
    else:
        profile = Profile.objects.get(user_id=id)
        context = {'profile': profile, 'user': user}
        return render(request, 'userprofile/info_local.html', context)
