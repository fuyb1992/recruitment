from django.shortcuts import render,redirect
from .forms import *
# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse,HttpResponseRedirect
from random import choice
import string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from jobs import settings
import xlrd
# from duals.models import *
from django.contrib import messages
def my_login(request):
    redirect_to = request.GET.get('next')
    if  not redirect_to:
        redirect_to=reverse('post:show_positions')
    if request.method == 'POST':
        form = LoginForm(data=request.POST, auto_id="%s")
        if form.is_valid():
            data = form.clean()
            user = authenticate(request,username=data['username'].strip(), password=data['password'])
#             bk = xlrd.open_workbook('学校码表.xlsx')
#             sh = bk.sheet_by_name('学校')
#             nrows = sh.nrows
#             for i in range(1, nrows):
#                 name = sh.cell_value(i, 0)
#                 pc = sh.cell_value(i, 3)
#                 try:
#                     schools.objects.create(name=name,pc=pc)
#                 except BaseException as e:
#                     print (e)
#             print ('finished!')
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                login_errors='密码有误'
    else:
        form = LoginForm(auto_id="%s")
    return render(request, 'accounts/login.html', locals())
def signup(request):
    redirect_to = request.GET.get('next')
    if not redirect_to or redirect_to==reverse('accounts:login'):
        redirect_to=reverse('post:show_positions')
    path=request.get_full_path()
    if request.method=='POST':
        form=SignupForm(data=request.POST,auto_id="%s")
        if form.is_valid():
            UserModel=get_user_model()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user=UserModel.objects.create_user(username=username,email=email,password=password)
            user.save()
            auth_user = authenticate(username=username,password=password)
            login(request,auth_user)
            messages.add_message(request, messages.INFO, '账号注册成功！')
            return HttpResponseRedirect(redirect_to)
    else:
        form=SignupForm(auto_id="%s")
    return render(request,'accounts/signup.html',locals())
def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form= ChangeForm(request.POST)
            if form.is_valid():
                confirm_password = form.clean_confirm_password()
                User.objects.filter(username=request.user.username).update(password=make_password(confirm_password))  ##如果用户名、原密码匹配则更新密码
                return redirect(reverse('accounts:login'))
        else:
            form = ChangeForm()
        return render(request,'accounts/change.html', locals())
    else:
        return redirect(reverse('accounts:login'))
def GenPassword(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])
def forget_password(request):
    if request.method == 'POST':
            form= ForgetPasswordForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email= form.clean_email()
                password=GenPassword(8)
                try:
                    send_mail('密码重置', '您好,您的密码重置为{0}，请登录后及时更改密码！'.format(password), settings.DEFAULT_FROM_EMAIL,[email], fail_silently=False)
                    User.objects.filter(username=username).update(password=make_password(password))  ##如果用户名、原密码匹配则更新密码
                except:
                    warning_message='密码重置失败，请联系管理员！'
                warning_message='密码重置成功，请注意查收您的邮箱！'
    else:
        form = ForgetPasswordForm()
    return render(request,'accounts/getpassword.html', locals())