from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from post.models import positions
from accounts.models import provience
from django.contrib.auth.models import User
# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from interview.models import *
from .forms import *
from django.shortcuts import render_to_response
from django.forms import formset_factory,modelformset_factory
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dal import autocomplete
from django.db import IntegrityError

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph,Spacer,Table,Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_RIGHT
from reportlab.lib.units import inch
from io import BytesIO
import time
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib import colors
from django.contrib.admin import widgets
from pytz import timezone
from jobs import settings
from datetime import datetime
settings_time_zone = timezone(settings.TIME_ZONE)
@login_required(login_url='/accounts/login/')
def base_info_view(request,id='-1',pro='-1'):
    if not base_info.objects.filter(cuser=request.user) and (id=='-1' or pro=='-1'):
        messages.add_message(request, messages.WARNING, '请先选择岗位，后填写简历！')
        return redirect(reverse('post:show_positions'))
    if appointment.objects.filter(app_user=base_info.objects.filter(cuser=request.user)):
        messages.add_message(request, messages.ERROR, '您已投递%s岗位，且已被受理，现无法更改简历或投递其它岗位！' % base_info.objects.get(cuser=request.user).position)
        return redirect(reverse('post:show_positions'))
    base_infoFormSet=modelformset_factory(base_info,form=base_infoForm, max_num=1)
    #base_infoFormSet=formset_factory(base_infoForm, max_num=1)
    if id!='-1' and pro!='-1':
        pos=positions.objects.get(pk=id)
        prov=provience.objects.get(pk=pro)
        messages.add_message(request, messages.WARNING, '您选择的是 %s--%s岗位，简历投递受理后将无法修改简历或岗位，请您慎重填写。' % (prov,pos))
    else:
        messages.add_message(request, messages.INFO, '您已投递 %s--%s岗位。' % (base_info.objects.get(cuser=request.user).provience_applied,base_info.objects.get(cuser=request.user).position))
    if request.method=='POST':
        formset=base_infoFormSet(request.POST,request.FILES)
        if formset.is_valid():
            for form in formset:
                instance=form.instance
                instance.cuser=request.user
                if id!='-1' and pro!='-1':
                    instance.position=pos
                    instance.provience_applied=prov
                try:
                    instance.save()
                except IntegrityError:
                  messages.add_message(request, messages.ERROR, '下列各项不能为空！')
                  return render(request,'cv/base_info.html', locals())
            return redirect(reverse('cv:education_info'))

    else:
        formset=base_infoFormSet(queryset=base_info.objects.filter(cuser=request.user))
    return render(request,'cv/base_info.html', locals())
class MySelectDateWidget(forms.SelectDateWidget):
    def get_context(self, *args, **kwargs):
        old_state = self.is_required
        self.is_required = False
        context = super(MySelectDateWidget, self).get_context(*args, **kwargs)
        self.is_required = old_state
        return context
@login_required(login_url='/accounts/login/')
def education_info_view(request):
    this_year = datetime.now().year
    education_infoFormSet=modelformset_factory(education_info,fields=('degree','school', 'major', 'start_date', 'end_date', 'activities','awards'),
                                               widgets = {'school':autocomplete.ModelSelect2(url='schools-autocomplete'),'start_date':MySelectDateWidget(years=range(this_year,2000,-1)),'end_date':MySelectDateWidget(years=range(this_year,2000,-1)),}, max_num=10, extra=1)
    if request.method=='POST':
        formset=education_infoFormSet(request.POST,request.FILES)
        if formset.is_valid():
            instances=formset.save(commit=False)
            for instance in instances:
                instance.name=base_info.objects.get(cuser=request.user)
                instance.save()
            return redirect(reverse('cv:work_info'))

    else:
        formset=education_infoFormSet(queryset=education_info.objects.filter(name=base_info.objects.filter(cuser=request.user)))
    return render(request,'cv/education_info.html', {'formset': formset})
@login_required(login_url='/accounts/login/')
def work_info_view(request):
    this_year = datetime.now().year
    work_infoFormset=modelformset_factory(work_info,exclude=('cuser',),widgets = {'start_date':MySelectDateWidget(years=range(this_year,2000,-1)),'end_date':MySelectDateWidget(years=range(this_year,2000,-1)),}, max_num=10, extra=1)
    if request.method=='POST':
        formset=work_infoFormset(request.POST,request.FILES)
        if formset.is_valid():
            instances=formset.save(commit=False)
            for instance in instances:
                instance.name=base_info.objects.get(cuser=request.user)
                instance.save()
            return redirect(reverse('interview:show_process'))
    else:
        formset=work_infoFormset(queryset=work_info.objects.filter(name=base_info.objects.filter(cuser=request.user)))
    return render(request,'cv/work_info.html', {'formset': formset})


pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
def commify(n):
    """
    Add commas to an integer `n`.

        >>> commify(1)
        '1'
        >>> commify(123)
        '123'
        >>> commify(1234)
        '1,234'
        >>> commify(1234567890)
        '1,234,567,890'
        >>> commify(123.0)
        '123.0'
        >>> commify(1234.5)
        '1,234.5'
        >>> commify(1234.56789)
        '1,234.56789'
        >>> commify('%.2f' % 1234.5)
        '1,234.50'
        >>> commify(None)
        >>>

    """
    if n is None: return None
    n = str(n)
    if '.' in n:
        dollars, cents = n.split('.')
    else:
        dollars, cents = n, None

    r = []
    for i, c in enumerate(str(dollars)[::-1]):
        if i and (not (i % 3)):
            r.insert(0, ',')
        r.insert(0, c)
    out = ''.join(r)
    if cents:
        out += '.' + cents
    return out
def ture_or_false(value):
    if value:
        return '是'
    else:
        return '否'
class MyPrint(object):
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
    def print(self,obj):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='my_head',fontName='STSong-Light', fontSize=22,leading=42,alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='my_para',fontName="STSong-Light",fontSize=8,leading=10))
        I=Image(obj.photo,0.8*inch,1.2*inch)
        elements.append(Paragraph('中公教育应聘人员登记表', styles['my_head']))
        P=Paragraph('尊敬的应聘者：<br/>欢迎您应聘中公教育集团！为了更全面深入地了解您的个人情况，请您本着诚信的原则，如实填写以下信息。我们将采用多种方式对您的学历、工作经历、薪资等重点信息进行核实，并将此作为最终是否录用的重要依据。本表资料我们将严格保密，谢谢您的配合！', styles['my_para'])
        data=[
            [P,'','','','填表日期'+'\n'+obj.update_time.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M"),I],
            ['基本信息','','','','',''],
            ['应聘渠道：',obj.channel,'应聘岗位：',obj.position,'应聘省份:',obj.provience_applied],
            ['姓名：',obj.name,'性别：',obj.get_sex_display(),'民族：',obj.get_minzu_display()],
            ['手机：',obj.phone_num,'电子邮箱：',User.objects.get(username=obj.cuser).email,'婚姻状况：',obj.get_marital_status_display()],
            ['政治面貌：',obj.get_politics_status_display(),'身份证号：',obj.id_num,'籍贯：',obj.get_provience_display()],
            ['外语语种：',obj.language,'外语水平：',obj.language_leve,'教师资格证：',ture_or_false(obj.teacher_cert)],
            ['是否有亲戚、朋友在本公司工作。□无   □有','','姓名：','','部门：','关系：'],
            ['是否有过不良行为记录？请详细告知。□无  □有  缘由：','','','','',''],
            ['是否曾遭受过重大疾病或有家族遗传病史？请详细告知。□无  □有  名称：','','','','',''],
            ['请依次选出三项能够影响您选择工作的关键因素：A. 能力迅速提升的机会 B. 薪酬福利 C. 培训机会 D. 稳定的工作\nE. 和谐的工作氛围 F. 企业的发展前景 G. 学习公务员考试知识（按照优先级从高到低顺序列举三个）', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['教育经历', '', '', '', '', ''],
            ['起始日期','结束日期','毕业院校','所学专业','学历','在校期间获得的证书'],
            ]

        edus=education_info.objects.filter(name=obj)
        i=13
        ts = [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
              ('FONT', (0, 0), (-1, -1), 'STSong-Light'),
              ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
              ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
              ('FONTSIZE', (0, 0), (-1, -1), 8),
              ('LEADING', (0, 0), (-1, -1), 10),
              ('SPAN', (0, 0), (3, 0)),
              ('SPAN', (0, 7), (1, 7)),
              ('SPAN', (0, 8), (-1, 8)),
              ('SPAN', (0, 9), (-1, 9)),
              ('SPAN', (0, 10), (-1, 11)),
              ('SPAN', (0, 12), (-1, 12)),
              ('FONTSIZE', (0, 12), (-1, 12), 12),
              ('LEADING', (0, 12), (-1, 12), 15),
              ('ALIGN', (0, 12), (-1, 12), 'CENTER'),
              ('SPAN', (0, 1), (4, 1)),
              ('FONTSIZE', (0, 1), (-1, 1), 12),
              ('LEADING', (0, 1), (-1, 1), 15),
              ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
              ('SPAN',(-1,0),(-1,1)),
              ]
        for edu in edus:
            P = Paragraph(edu.awards, styles['my_para'])
            Pschool=Paragraph(edu.school.name+' '+edu.school.pc, styles['my_para'])
            data.append([edu.start_date,edu.end_date,Pschool,edu.major,edu.get_degree_display(),P])
            P=Paragraph(edu.activities, styles['my_para'])
            data.append(['在校期间的活动',P,'','','',''])
            i+=2
            ts.append(('SPAN', (1, i), (-1, i)))
        edu_end=i+1
        ts.append(('FONTSIZE', (0, edu_end), (-1, edu_end), 12))
        ts.append(('LEADING', (0, edu_end), (-1, edu_end), 15))
        ts.append(('ALIGN', (0, edu_end), (-1, edu_end), 'CENTER'))
        ts.append(('SPAN', (0, edu_end), (-1, edu_end)))

        data.append(['工作/实习经历', '', '', '', '', ''])
        data.append(['起始日期','结束日期','公司名称','','职位',''])
        ts.append(('SPAN', (2, edu_end + 1), (3, edu_end + 1)))
        ts.append(('SPAN', (4, edu_end + 1), (5, edu_end + 1)))
        i+=2
        works=work_info.objects.filter(name=obj)
        for work in works:
            P = Paragraph(work.activities, styles['my_para'])
            data.append([work.start_date,work.end_date,work.company,'',work.position,''])
            data.append(['主要工作内容',P,'','','',''])
            i+=1
            ts.append(('SPAN', (2, i), (3, i)))
            ts.append(('SPAN', (4, i), (5, i)))
            i+=1
            ts.append(('SPAN', (1, i), (-1, i)))
        data.append(['期望薪金（元/月）：',obj.salary_except,'','','',''])
        P = Paragraph('本人声明所提供一切信息均属实且准确，且同意公司对本人所提供信息作核查，如有隐瞒或虚假，公司有权即时解聘本人而无需做出任何赔偿。', styles['my_para'])
        data.append([P,'','','','',''])
        ts.append(('SPAN', (0, i+2), (-1, i+2)))
        data.append(['签名：','','','','日期：','                 年       月       日'])
        table=Table(data,6*15,style=ts)
        elements.append(table)
        doc.build(elements)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
    def interview(self,obj):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(name='my_head', fontName='STSong-Light', fontSize=22, leading=42, alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='my_para', fontName="STSong-Light", fontSize=8, leading=10))

        elements.append(Paragraph('中公教育应聘面试记录', styles['my_head']))
        inters=interview.objects.filter(inter_user=obj)
        data=[
            ['基本信息','','','','',''],
            ['应聘者姓名：',obj.name,'手机号：',obj.phone_num,'邮箱：',User.objects.get(username=obj.cuser).email],
            ['面试记录','','','','',''],
            ['应聘岗位','面试类型','面试官姓名','面试要点','得分','填写时间'],
            ]
        ts = [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
              ('FONT', (0, 0), (-1, -1), 'STSong-Light'),
              ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
              ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
              ('FONTSIZE', (0, 0), (-1, -1), 8),
              ('LEADING', (0, 0), (-1, -1), 10),
              ('SPAN', (0, 0), (-1, 0)),
              ('FONTSIZE', (0, 0), (-1, 0), 12),
              ('LEADING', (0, 0), (-1, 0), 15),
              ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
              ('SPAN', (0, 2), (-1, 2)),
              ('FONTSIZE', (0, 2), (-1, 2), 12),
              ('LEADING', (0, 2), (-1, 2), 15),
              ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
              ]
        i=3
        for inter in inters:
            P=Paragraph(inter.remark, styles['my_para'])
            data.append([inter.position,inter.inter_cho,inter.cuser.last_name+inter.cuser.first_name,inter.point,inter.grade,inter.update_time.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M")])
            data.append(['评语',P,'','',''])
            i+=2
            ts.append(('SPAN', (1, i), (-1, i)))
        table=Table(data,6*15,style=ts)
        elements.append(table)
        doc.build(elements)
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
def partpdf(request,id):
    if request.user.is_staff:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cv_%s.pdf"'%id

        buffer = BytesIO()

        report = MyPrint(buffer, 'A4')
        obj=base_info.objects.get(pk=id)
        pdf = report.print(obj)

        response.write(pdf)
        return response
    else:
        return HttpResponse('无权限')
def interviewpdf(request,id):
    if request.user.is_staff:

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="interview_%s.pdf"'% id

        buffer = BytesIO()

        report = MyPrint(buffer, 'A4')
        obj = base_info.objects.get(pk=id)
        pdf = report.interview(obj)

        response.write(pdf)
        return response
    else:
        return HttpResponse('无权限')