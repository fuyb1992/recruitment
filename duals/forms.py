#coding: UTF-8
'''
Created on 2017年8月12日

@author: Fu Yingbin, 浮颖彬
'''
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *
from dal import autocomplete

class dualmessagesForm(ModelForm):
    class Meta:
        model = dualmessages
        exclude=['update_time']
        widgets = {
            'school':autocomplete.ModelSelect2(url='schools-autocomplete'),
        }