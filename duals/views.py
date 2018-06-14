from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from .models import *
from .forms import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login




num_each_page=30
def show_dualmessages(request):
    proviences = provience.objects.all()
    mes_list = dualmessages.objects.filter(post=True).order_by('-update_time')
    paginator = Paginator(mes_list, num_each_page)
    page = request.GET.get('page')
    try:
        mes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        mes = paginator.page(paginator.num_pages)
    if request.method=="POST":
        if request.user.is_authenticated:
            check_box_list=request.POST.getlist('check_box_list')
            if check_box_list:
                num_add=0
                for check in check_box_list:
                    user_dual_exit=user_dual.objects.filter(dual=dualmessages.objects.get(pk=check))
                    if not user_dual_exit:
                        user_dual.objects.create(cuser=request.user,dual=dualmessages.objects.get(pk=check))
                        num_add+=1
                warning_message='{0}条信息成功添加至我的双选会！'.format(num_add)
                return render(request, 'duals\show_dualmessages.html', locals())
            else:
                warning_message = '请至少勾选一条信息！'
                return render(request, 'duals\show_dualmessages.html', locals())
        else:
            warning_message = '请先登录！'
            return render(request, 'duals\show_dualmessages.html', locals())

    else:
        warning_message=''
        return render(request, 'duals\show_dualmessages.html', locals())
def show_dualmessages_filter(request,pro):
    proviences = provience.objects.all()
    if pro:
        mes_list = dualmessages.objects.filter(post=True).filter(provience=pro).order_by('-update_time')
    else:
        mes_list = dualmessages.objects.filter(post=True).order_by('-update_time')
    paginator = Paginator(mes_list, num_each_page)
    page = request.GET.get('page')
    try:
        mes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        mes = paginator.page(paginator.num_pages)
    if request.method == "POST":
        if request.user.is_authenticated:
            check_box_list = request.POST.getlist('check_box_list')
            if check_box_list:
                num_add = 0
                for check in check_box_list:
                    try:
                        user_dual.objects.create(cuser=request.user, dual=dualmessages.objects.get(pk=check))
                        num_add += 1
                    except:
                        pass
                warning_message = '{0}条信息成功添加至我的双选会！'.format(num_add)
                return render(request, 'duals\show_dualmessages.html', locals())
            else:
                warning_message = '请至少勾选一条信息！'
                return render(request, 'duals\show_dualmessages.html', locals())
        else:
            warning_message = '请先登录！'
            return render(request, 'duals\show_dualmessages.html', locals())

    else:
        warning_message = ''
        return render(request, 'duals\show_dualmessages.html', locals())
def show_userdual(request):
    if request.user.is_authenticated:
        mes_list=user_dual.objects.filter(cuser=request.user).order_by('-dual__preferred_date')
        paginator = Paginator(mes_list, num_each_page)
        page = request.GET.get('page')
        try:
            mes = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            mes = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            mes = paginator.page(paginator.num_pages)
        return render(request, 'duals\show_userdual.html', locals())
    else:
        warning_message = '请先登录！'
        return render(request, 'duals\show_userdual.html', locals())
class user_dualUpdate(UpdateView):
    models=user_dual
    fields=['dual','dual_status','person_attend','comment']

    def get_queryset(self):
        return user_dual.objects.filter(pk=self.kwargs['pk'])

    def form_valid(self, form):
        self.object = form.save()
        return redirect('show_userdual')