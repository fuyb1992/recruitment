from django.db import models
from accounts.models import provience,department
from django.contrib.auth.models import User
from random import choice
# Create your models here.
pos_choice=(('a','全职'),('b','兼职'),('c','实习'))
class position_category(models.Model):
    name=models.CharField('岗位类别',max_length=20)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='岗位类别'
        verbose_name_plural='岗位类别管理'
class positions(models.Model):
    name=models.CharField('岗位名称',max_length=20)
    dep=models.ManyToManyField(department,verbose_name="招聘部门")
    pro=models.ManyToManyField(provience,verbose_name="招聘省份")
    position_requirements=models.TextField('岗位要求',max_length=500)
    position_statement=models.TextField('岗位描述',max_length=500)
    position_annual_salay_up=models.PositiveIntegerField('年薪上限',null=True,blank=True)
    position_annual_salay_down=models.PositiveIntegerField('年薪下限',null=True,blank=True)
    position_monthly_salary_up=models.PositiveIntegerField('月薪上限',null=True,blank=True)
    position_monthly_salary_down=models.PositiveIntegerField('月薪下限',null=True,blank=True)
    recruiting_numbers=models.PositiveSmallIntegerField('招聘人数')
    category=models.ForeignKey(position_category,verbose_name='岗位类别')
    property=models.CharField('岗位性质',max_length=1,choices=pos_choice,default='a')
    post_status=models.BooleanField('发布状态')
    sort_value=models.PositiveSmallIntegerField('显示顺序',default=0)
    update_date=models.DateTimeField('更新时间',auto_now_add=True,editable=True)
    def __str__(self):
        return self.name
    def getdep(self):
        return ','.join([obj.name for obj in self.dep.all()])
    getdep.short_description='招聘部门'
    def getpro(self):
        if len(self.pro.all())>30:
            return '全国(西藏、港澳台除外）'
        else:
            return ','.join([obj.name for obj in self.pro.all()])
    getpro.short_description='招聘省份'
    class Meta:
        verbose_name='岗位发布'
        verbose_name_plural='岗位发布管理'
