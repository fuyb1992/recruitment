from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from cv.models import base_info
from post.models import *
from datetime import datetime
class interview_choices(models.Model):
    name=models.CharField('面试类型名称',max_length=10)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '面试类型名称'
        verbose_name_plural = '面试类型名称管理'
class interview_base(models.Model):
    inte_cho=models.ForeignKey(interview_choices,verbose_name='面试类型')
    point=models.CharField('面试要点',max_length=20)
    help_message=models.TextField('要点范例',max_length=200,blank=True,null=True)
    require_status=models.BooleanField('是否为必填项')
    status=models.BooleanField('发布要点')
    def __str__(self):
        return self.point
    class Meta:
        verbose_name = '面试要点'
        verbose_name_plural = '面试要点管理'
class interview(models.Model):
    cuser=models.ForeignKey(User,verbose_name='面试官用户名',null=True,blank=True)
    inter_user=models.ForeignKey(base_info,editable=False,verbose_name='面试者姓名', related_name='inervewer_related')
    position=models.CharField('应聘岗位',max_length=50,editable=False)
    inter_cho=models.ForeignKey(interview_choices,verbose_name='面试类型')
    point=models.ForeignKey(interview_base,verbose_name='面试要点')
    remark=models.TextField('面试评语',max_length=200)
    grade=models.FloatField('得分')
    update_time=models.DateTimeField('填写时间',auto_now_add=True)
    def __str__(self):
        try:
            return '面试官：'+self.cuser.last_name+self.cuser.first_name+',应聘岗位：'+self.position
        except:
            return '无当前用户姓名'
    class Meta:
        verbose_name = '面试评语'
        verbose_name_plural = '面试评语管理'
class appointment_user(models.Model):
    cuser=models.ForeignKey(User,verbose_name='用户名',editable=False, related_name='appointment_user_related',null=True,blank=True)
    address=models.CharField('地址',max_length=50)
    contact_person=models.CharField('联系人',max_length=10)
    contact_phone=models.CharField('联系电话',max_length=20)
    def __str__(self):
        return self.contact_person+' '+self.address+' '+self.contact_phone
    class Meta:
        verbose_name = '联系方式'
        verbose_name_plural = '联系方式管理'
class appointment(models.Model):
    cuser=models.ForeignKey(User,verbose_name='约面人用户名', related_name='appointment_related',null=True,blank=True)
    app_user=models.ForeignKey(base_info,editable=False, related_name='appointment_base_related',verbose_name='面试者姓名')
    inte_cho=models.ForeignKey(interview_choices,verbose_name='面试类型')
    app_date=models.DateTimeField('面试时间')
    contact=models.ForeignKey(appointment_user,verbose_name='联系人/地址/电话')
    check_in=models.NullBooleanField('如约参加面试')
    remark=models.CharField('备注',max_length=50,blank=True,null=True)
    update_date=models.DateTimeField('预约时间',auto_now_add=True)
    def __str__(self):
        try:
            return self.cuser.last_name+self.cuser.first_name
        except:
            return '无当前用户姓名'
    class Meta:
        verbose_name = '面试预约'
        verbose_name_plural = '面试预约管理'
class mail_template(models.Model):
    pos_cat=models.OneToOneField(position_category,verbose_name='使用岗位类别')
    template_context=models.TextField('邮件模板内容',max_length=2000)
    def __str__(self):
        return self.pos_cat.name
    class Meta:
        verbose_name = '约面邮件模板'
        verbose_name_plural = '约面邮件模板管理'
class other_mail_template(models.Model):
    mail_cat=models.CharField('模板类型',max_length=20)
    template_context=models.TextField('邮件模板内容',max_length=2000)
    def __str__(self):
        return self.mail_cat
    class Meta:
        verbose_name = '其它邮件模板'
        verbose_name_plural = '其它邮件模板管理'
class offer_ready(models.Model):
    cuser=models.ForeignKey(User,verbose_name='负责人用户名',null=True,blank=True)
    offer_user=models.OneToOneField(base_info,editable=False,verbose_name='应聘者姓名',related_name='offer_ready_base_info')
    ready=models.BooleanField('提交预入职')
    comment = models.CharField('备注', max_length=200,null=True, blank=True)
    update_date=models.DateTimeField('提交时间',auto_now_add=True,editable=True)
    def __str__(self):
        try:
            return self.cuser.last_name+self.cuser.first_name
        except:
            return '无当前用户姓名'
    class Meta:
        verbose_name = '提交预入职'
        verbose_name_plural = '提交预入职管理'
class offer_approval(models.Model):
    cuser=models.ForeignKey(User,verbose_name='负责人用户名',null=True,blank=True)
    offer_user=models.OneToOneField(base_info,editable=False,verbose_name='应聘者姓名',related_name='offer_approval_base_info')
    approval=models.BooleanField('预入职审核通过')
    comment=models.CharField('备注',max_length=200,null=True,blank=True)
    update_date=models.DateTimeField('提交时间',auto_now_add=True,editable=True)
    def __str__(self):
        try:
            return self.cuser.last_name+self.cuser.first_name
        except:
            return '无当前用户姓名'
    class Meta:
        verbose_name = '预入职审核'
        verbose_name_plural = '预入职审核管理'
class contract(models.Model):
    name=models.CharField('合同类型',max_length=20)
    def __str__(self):
        return  self.name
    class Meta:
        verbose_name='合同类型'
        verbose_name_plural='合同类型管理'
class in_service(models.Model):
    cuser = models.ForeignKey(User, verbose_name='负责人用户名', null=True, blank=True)
    offer_user = models.OneToOneField(base_info, editable=False, verbose_name='应聘者姓名', related_name='in_sesrvice_base_info')
    date_predict=models.DateField('预计签订劳动合同日期',null=True,blank=True)
    contract=models.ForeignKey(contract,verbose_name='合同类型',null=True,blank=True)
    on_board=models.NullBooleanField('是否如约签订劳动合同')
    date_in=models.DateField('签订劳动合同日期',null=True,blank=True)
    def __str__(self):
        return self.offer_user.name
    class Meta:
        verbose_name='入职信息'
        verbose_name_plural='入职管理'