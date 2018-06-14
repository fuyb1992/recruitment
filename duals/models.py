from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
from accounts.models import provience
from django.template.defaultfilters import default
class schools(models.Model):
    name=models.CharField('学校名称',max_length=30)
    pc=models.CharField('批次',max_length=10)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='高校'
        verbose_name_plural='高校管理'
status_choices=(
    ('1','未报名'),
    ('2','已报名'),
    ('3','学校审核通过'),
    ('4','学校审核未通过'),
    )
class dualmessages(models.Model):
    name=models.CharField('双选会名称',max_length=100)
    school=models.ForeignKey(schools,on_delete=models.CASCADE,verbose_name='主办高校')
    update_time=models.DateTimeField('更新日期',auto_now_add=True)
    deadline=models.DateField('报名截止日期',null=True,blank=True)
    preferred_date=models.DateTimeField('举办日期',null=True,blank=True)
    provience=models.ForeignKey(provience,verbose_name='省份')
    address=models.CharField('举办地址',max_length=100,null=True,blank=True)
    url_adress=models.CharField('链接',max_length=200,null=True,blank=True)
    cost=models.PositiveSmallIntegerField('报名费',null=True,blank=True)
    post=models.CharField('状态',max_length=1,choices=status_choices,default='1')
    person_attend=models.CharField('参加人',max_length=20,null=True,blank=True)
    cv_num=models.PositiveSmallIntegerField('简历数',null=True,blank=True)
    ks=models.NullBooleanField('是否跨省')
    comment=models.CharField('备注',max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='双选会信息'
        verbose_name_plural='双选会信息管理'
class user_dual(models.Model):
    cuser=models.ForeignKey(User)
    dual=models.ForeignKey(dualmessages,verbose_name='双选会名称')
    dual_status=models.CharField('状态',max_length=1,choices=(('a','未报名'),('b','审核中'),('c','审核通过'),('d','已参加'),('e','活动取消'),('f','其它'),),null=True,blank=True)
    person_attend=models.CharField('参加人',max_length=20,null=True,blank=True)
    comment=models.CharField('备注',max_length=100,null=True,blank=True)
    def __str__(self):
        return self.cuser.username
    def get_absolute_url(self):
        return reverse('user_dual-detail', kwargs={'pk': self.pk})
    class Meta:
        verbose_name='用户双选会信息'
        verbose_name_plural='用户双选会信息管理'