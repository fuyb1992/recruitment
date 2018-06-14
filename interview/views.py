from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from cv.models import *
from interview.models import *
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='/accounts/login/')
def show_process(request):
    status=0

    if base_info.objects.filter(cuser=request.user):
        bi=base_info.objects.get(cuser=request.user)
        status=1
        if offer_approval.objects.filter(offer_user=bi):
            status=4
        elif interview.objects.filter(inter_user=bi):
            status=3
        elif appointment.objects.filter(app_user=bi):
            status=2
    return render(request,'interview/show_process.html', locals())
def requ(para):
    if para:
        return '--必填'
    else:
        return ''
def getPoints(request,cho):
    try:
        cho_instance=interview_choices.objects.get(pk=cho)
        interview_base_str=[(ib.id, str(ib.point)+requ(ib.require_status)) for ib in interview_base.objects.filter(status=True).filter(inte_cho=cho_instance).order_by('-require_status')]
        interview_base_str.insert(0, ('', '----'))
        return JsonResponse({'points':interview_base_str})
    except:
        return JsonResponse({'points':[('', '----')]})
def getHelpMessage(request,point):
   
    help_message=interview_base.objects.get(pk=point).help_message
    return JsonResponse({'help_message':help_message})
        