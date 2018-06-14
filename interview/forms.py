from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
#from crequest.middleware import CrequestMiddleware#pip install django-crequest
#def requ(para):
#    if para:
#        return '--必填'
#    else:
#        return ''
#interview_base_str=[(ib.id, str(ib.inte_cho)+'--'+str(ib.point)+requ(ib.require_status)) for ib in interview_base.objects.filter(status=True)]
#interview_base_str.insert(0, ('', '----'))
class interviewInlineForm(forms.ModelForm):
    grade=forms.FloatField(min_value=0.0, max_value=10.0,widget=forms.NumberInput(attrs={'placeholder':'10分制:6分及格,9分优秀'}))
    inter_cho=forms.ModelChoiceField(queryset=interview_choices.objects.all(),widget=forms.Select(attrs={'onchange':'get_point(this.id)'}))
    point=forms.ModelChoiceField(queryset=interview_base.objects.all(),widget=forms.Select(attrs={'onchange':'getHelpMessage(this.id)','placeholder':'fuck'}))
    def __init__(self, *args, **kwargs):
        super(interviewInlineForm, self).__init__(*args, **kwargs)
        self.fields['cuser'].queryset = User.objects.filter(is_staff=True)
        #self.fields['point'].choices=interview_base_str
class appointmentInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(appointmentInlineForm, self).__init__(*args, **kwargs)
        self.fields['cuser'].queryset = User.objects.filter(is_staff=True)
#         request = CrequestMiddleware.get_request()
#         self.fields['contact'].queryset = appointment_user.objects.filter(cuser=request.user)
class offer_readyInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(offer_readyInlineForm, self).__init__(*args, **kwargs)
        self.fields['cuser'].queryset = User.objects.filter(is_staff=True)
class offer_approvalInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(offer_approvalInlineForm, self).__init__(*args, **kwargs)
        self.fields['cuser'].queryset = User.objects.filter(is_staff=True)


