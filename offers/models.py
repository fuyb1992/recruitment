from django.db import models
from post.models import positions
from accounts.models import provience as pro
from accounts.models import department
from duals.models import schools
from django.template.defaultfilters import default
from cv.models import minzu_choices
# Create your models here.
degree_choices=(
    ('a','专科'),
    ('b','本科'),
    ('c','硕士'),
    ('d','博士'),
    ('e','本科(双学位)'),
    ('f','其它')
    )
labour_choices=(
    ('a','劳动合同'),
    ('b','实习协议'),
    ('c','兼职协议')
    )
to_beijing_station_choices=(
    ('a','北京西站'),
    ('b','北京站'),
    ('c','北京南站'),
    ('d','北京北站')
    )
class channels(models.Model):
    name=models.CharField('应聘渠道',max_length=10)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '应聘渠道'
        verbose_name_plural = '应聘渠道管理'
class candidates(models.Model):
    photo=models.ImageField("照片",upload_to='photos/%Y/%m/%d',null=True,blank=True)
    channel=models.ForeignKey(channels,verbose_name='应聘渠道')
    other_channel=models.CharField('其它应聘渠道',max_length=50,null=True,blank=True)
    provience_applied=models.ForeignKey(pro,verbose_name='申请分校',related_name='cand_applied')
    provience_work=models.ForeignKey(pro,verbose_name='工作地点',related_name='cand_work')
    name=models.CharField('姓名',max_length=10)
    work_id=models.CharField('工号',max_length=20,null=True,blank=True)
    id_num=models.CharField('身份证号',max_length=18,primary_key=True)
    minzu=models.CharField('民族',max_length=2,choices=minzu_choices)
    phone_num=models.CharField('手机号',max_length=11)
    email=models.CharField('邮箱',max_length=60)
    first_school=models.ForeignKey(schools,verbose_name='第一学历毕业院校',null=True,blank=True,related_name='cand_first_school')
    first_major=models.CharField('第一学历专业',max_length=60,null=True,blank=True)
    finnal_school=models.ForeignKey(schools,verbose_name='最终学历毕业院校',related_name='cand_finnal_school')
    finnal_major=models.CharField('最终学历专业',max_length=60)
    finnal_degree=models.CharField('最终学历',max_length=1,choices=degree_choices)
    graduation_date=models.DateField('毕业日期')
    teacher_cert=models.BooleanField('教师资格证')
    probation_salary=models.PositiveIntegerField('试用期基本工资（元/月）')
    subsidy=models.PositiveIntegerField('试用期绩效/培训补助（元/月）',null=True,blank=True)
    teaching_salary=models.PositiveIntegerField('课时费（元/时）',null=True,blank=True)
    salary_remark=models.BooleanField('薪金有无特殊')
    on_date=models.DateField('入职日期',null=True,blank=True)
    on_off=models.NullBooleanField('是否提交预入职',default=False)
    position=models.ForeignKey(positions,verbose_name='授课方向',related_name='cand_position')
    position_remarks=models.CharField('授课方向备注',max_length=100,null=True,blank=True)
    labour_class=models.CharField('用工类型',max_length=1,choices=labour_choices)
    train_direction=models.ForeignKey(positions,verbose_name='培训方向',related_name='cand_train_direction')
    train_direction_pro=models.ForeignKey(positions,verbose_name='分校上报的第一培训方向',null=True,blank=True,related_name='cand_train_direction_pro')
    train_confirm=models.BooleanField('是否参训')
    train_to_beijing=models.CharField('到京车次',max_length=10,null=True,blank=True)
    eta=models.DateTimeField('到京时间',null=True,blank=True)
    to_beijing_station=models.CharField('到京站',max_length=1,choices=to_beijing_station_choices,null=True,blank=True)
    computer_need=models.NullBooleanField('是否已领用电脑')
    remark=models.CharField('备注',max_length=100,null=True,blank=True)
    department=models.ForeignKey(department,verbose_name='所属部门',null=True,blank=True)
    direct_leader_hq=models.CharField('总部直属领导',max_length=10,null=True,blank=True)
    direct_leader_current=models.CharField('现直属领导',max_length=10,null=True,blank=True)
    positon_change_date=models.DateField('调架构时间',null=True,blank=True)
    finnal_interview=models.NullBooleanField('是否终审',null=True,blank=True)
    oral_defense=models.NullBooleanField('是否已毕业答辩',null=True,blank=True)
    oral_defense_date=models.DateField('答辩日期',null=True,blank=True)
    on_leave_date_start=models.DateField('预计请假日期起',null=True,blank=True)
    on_leave_date_end=models.DateField('预计请假日期至',null=True,blank=True)
    update_time=models.DateTimeField('填写时间',auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '候选人'
        verbose_name_plural = '预入职管理（临时）'