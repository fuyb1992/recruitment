from django.shortcuts import render,redirect
from django.urls import reverse
# Create your views here.
from django.views.generic import ListView
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse

num_each_page=20

def show_positions(request,pro='d',cat=100):
    pc=position_category.objects.all()
    cat=int(cat)
    if pro=='d':
        mes_list = positions.objects.filter(post_status=True)
    else:
        mes_list = positions.objects.filter(property=pro).filter(post_status=True)
    if cat==100:
        mes_list=mes_list.order_by('-sort_value')
    else:
        mes_list=mes_list.filter(category=cat).order_by('-sort_value')
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
    return render(request, 'post/positions_list.html', locals())
def show_proviences(request,id):
    position=positions.objects.filter(pk=id).filter(post_status=True).order_by('-sort_value')
    ptest='hello'
    return render(request,'post/proviences.html',locals())
    #return redirect(reverse('cv:base_info',kwargs={'id':id}))
# def to_cv(request,id,pro):
#     return redirect(reverse('cv:base_info', kwargs={'id': id,'pro':pro}))
def to_cv(request,id,pro):
    return redirect(reverse('cv:base_info', kwargs={'id': id,'pro':pro}))