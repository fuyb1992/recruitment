from django.contrib import admin
from .forms import *
from .models import *
from duals.models import schools
from post.models import positions
from accounts.models import provience as pro
from accounts.models import department as dep
from accounts.models import my_authority
from .forms import candidatesForm
from cv.models import minzu_choices
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin.templatetags.admin_list import date_hierarchy
import datetime
from import_export import resources
from import_export import fields
from pytz import timezone
from jobs import settings
from pip._vendor.distlib._backport.tarfile import TUREAD
from import_export.widgets import ForeignKeyWidget
settings_time_zone = timezone(settings.TIME_ZONE)
# Register your models here.
admin.site.register(channels)
def get_choices_values(obj,choices):
    for cho in choices:
        if cho[0]==obj:
            return cho[1]
class candidatesResource(resources.ModelResource):
    sex=fields.Field()
    age=fields.Field()
    minzu=fields.Field()
    finnal_degree=fields.Field()
    labour_class=fields.Field()
    update_time=fields.Field()
    channel=fields.Field(column_name='channel',attribute='channel',widget=ForeignKeyWidget(channels,'name'))
    first_school=fields.Field(column_name='first_school',attribute='first_school',widget=ForeignKeyWidget(schools,'name'))
    finnal_school=fields.Field(column_name='finnal_school',attribute='finnal_school',widget=ForeignKeyWidget(schools,'name'))
    position=fields.Field(column_name='position',attribute='position',widget=ForeignKeyWidget(positions,'name'))
    train_direction=fields.Field(column_name='train_direction',attribute='train_direction',widget=ForeignKeyWidget(positions,'name'))
    train_direction_pro=fields.Field(column_name='train_direction_pro',attribute='train_direction_pro',widget=ForeignKeyWidget(positions,'name'))
    provience_applied=fields.Field(column_name='provience_applied',attribute='provience_applied',widget=ForeignKeyWidget(pro,'name'))
    provience_work=fields.Field(column_name='provience_work',attribute='provience_work',widget=ForeignKeyWidget(pro,'name'))
    department=fields.Field(column_name='department',attribute='department',widget=ForeignKeyWidget(dep,'name'))
    '''def get_instance(self, instance_loader, row):
        """
        Calls the :doc:`InstanceLoader <api_instance_loaders>`.
        """
        for key,value in minzu_choices:
            if row['minzu'] in value:
                row['minzu']=key
                break
        for key,value in degree_choices:
            if row['finnal_degree'] in value:
                row['finnal_degree']=key
                break
        print (row)
        return instance_loader.get_instance(row)'''
        
    class Meta:
        model = candidates
        skip_unchanged=True
        report_skipped=True
        fields=('channel','other_channel','provience_applied','provience_work','name','work_id','sex','id_num','age','minzu','phone_num','email','first_school','first_major','first_school__pc',
                'finnal_school','finnal_major','finnal_degree','finnal_school__pc','graduation_date','teacher_cert','probation_salary','subsidy','teaching_salary','salary_remark','on_date','on_off',
                'position','position_remarks','labour_class','train_direction','train_direction_pro','train_confirm','train_to_beijing','eta','to_beijing_station','computer_need','remark','department','direct_leader_hq',
                'direct_leader_current','positon_change_date','finnal_interview','oral_defense','oral_defense_date','on_leave_date_start','on_leave_date_end','update_time',)
        export_order=('channel','other_channel','provience_applied','provience_work','name','work_id','sex','id_num','age','minzu','phone_num','email','first_school','first_major','first_school__pc',
                'finnal_school','finnal_major','finnal_degree','finnal_school__pc','graduation_date','teacher_cert','probation_salary','subsidy','teaching_salary','salary_remark','on_date','on_off',
                'position','position_remarks','labour_class','train_direction','train_direction_pro','train_confirm','train_to_beijing','eta','to_beijing_station','computer_need','remark','department','direct_leader_hq',
                'direct_leader_current','positon_change_date','finnal_interview','oral_defense','oral_defense_date','on_leave_date_start','on_leave_date_end','update_time',)
        import_id_fields = ('id_num', )
        widgets = {
                'graduation_date': {'format': '%Y-%m-%d'},
                }
    def get_export_headers(self):
        return ['应聘渠道','其它应聘渠道','提交分校','工作地点','姓名',u'工号',u'性别',u'身份证号码','年龄',u'民族'
               ,u'手机号',u'电子邮箱',u'第一学历毕业院校',u'第一学历专业','第一学历毕业院校批次',u'最终学历毕业院校',u'最终学历专业',u'最终学历',u'最终学历毕业院校批次'
               ,u'毕业日期',u'教师资格证',u'试用期基本工资',u'试用期绩效/培训补助',u'课时费',u'薪金有无特殊',u'入职日期','是否提交预入职',u'授课方向',u'备注',u'用工形式'
               ,u'培训方向',u'分校上报的第一培训方向',u'是否参训',u'到京车次',u'到京日期',u'到京站',u'是否已领用电脑',u'备注',u'所属部门'
               ,u'总部直属领导',u'现直属领导',u'调架构时间',u'是否终审',u'是否已完成毕业答辩',u'答辩时间',u'预请假日期起','预计请假日期至','时间戳']
    def dehydrate_sex(self,obj):
        id_num=obj.id_num
        if id_num:
            if int(id_num[17])%2:
                sex='男'
            else:
                sex='女'
        else:
            sex=' '
        return sex
    def dehydrate_age(self,obj):
        id_num=obj.id_num
        if id_num:
            age=round(datetime.datetime.now().year-int(id_num[6:10]))
        else:
            age=' '
        return age
    def dehydrate_minzu(self,obj):
        return get_choices_values(obj.minzu,minzu_choices)
    def dehydrate_finnal_degree(self,obj):
        return get_choices_values(obj.finnal_degree,degree_choices)
    def dehydrate_labour_class(self,obj ):
        return get_choices_values(obj.labour_class,labour_choices)
    def dehydrate_update_time(self,obj):
        update_time= obj.update_time
        if update_time:
            return update_time.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M")
        else:
            return ' '
class candidatesAdmin(ImportExportActionModelAdmin):
    resource_class=candidatesResource
    form=candidatesForm
    list_display=('name','get_sex','get_age','minzu','channel','provience_applied','position','phone_num','finnal_school','get_school_class','finnal_major','finnal_degree','on_date','on_off',)
    list_filter =('on_off','channel','provience_applied',)
    date_hierarchy='on_date'

    def get_sex(self,obj):
        id_num=obj.id_num
        if int(id_num[17])%2:
            sex='男'
        else:
            sex='女'
        return sex
    get_sex.short_description='性别'
    def get_age(self,obj):
        id_num=obj.id_num
        age=round(datetime.datetime.now().year-int(id_num[6:10]))
        return age
    get_age.short_description='年龄'
    def get_school_class(self,obj):
        pc=obj.finnal_school.pc 
        return pc
    get_school_class.short_description='学校批次'
    get_school_class.admin_order_field='finnal_school__pc '
    def get_queryset(self, request):
        """
        Filter the objects displayed in the change_list
        """
        qs = super(candidatesAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            ma=my_authority.objects.filter(admin_user=request.user)
            mp=ma.values('admin_authority_pro')
            md=ma.values('admin_authority_dep')
            p_list=[]
            d_list=[]
            if len(mp)>1:
                for i in range(0,len(mp)):
                    p_list.append(mp[i]['admin_authority_pro'])
                qs=qs.filter(provience_applied__in=p_list)
            else:
                qs=qs.filter(provience_applied=mp)
            if len(md)>1:
                for i in range(0,len(md)):
                    d_list.append(md[i]['admin_authority_dep'])
                qs=qs.filter(position__dep__in=d_list)
            else:
               qs=qs.filter(position__dep__in=md)
            return qs
admin.site.register(candidates,candidatesAdmin) 