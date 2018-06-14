from django.contrib import admin
from .models import *
from accounts.models import *
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from pytz import timezone
from jobs import settings
settings_time_zone = timezone(settings.TIME_ZONE)
# Register your models here.
class interviewResource(resources.ModelResource):
    name=fields.Field()
    update_time=fields.Field()
    class Meta:
        model = interview
        fields=('id','cuser__username','inter_user__name','position','inter_cho__name','point__point','remark','grade',)
        export_order=('id','cuser__username','name','inter_user__name','position','inter_cho__name','point__point','remark','grade','update_time',)
    def get_export_headers(self):
        return ['序号','面试官用户名','面试官姓名','应聘者姓名','意向岗位','面试类型','面试要点','评语','分数','填写时间']
    def dehydrate_name(self,obj):
        name=''
        try:
            name=obj.cuser.last_name+obj.cuser.first_name
        except:
            name='该用户未登记姓名'
        return name
    def dehydrate_update_time(self,obj):
        return obj.update_time.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M")
class interviewAdmin(ImportExportActionModelAdmin):
    list_display = ('cuser','show_name','inter_user','position','inter_cho','point','remark','grade','update_time',)
    list_filter=('inter_cho','point','update_time',)
    resource_class=interviewResource
    def show_name(self,obj):
        name=''
        try:
            name=obj.cuser.last_name+obj.cuser.first_name
        except:
            name='该用户未登记姓名'
        return name
    show_name.short_description='面试官姓名'
    def get_queryset(self, request):
        qs = super(interviewAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
           qs=qs.filter(cuser=request.user) 
        return qs
admin.site.register(interview,interviewAdmin)
class interview_choicesAdmin(admin.ModelAdmin):
    list_display = ('id','name',)

admin.site.register(interview_choices,interview_choicesAdmin)
class interview_baseAdmin(admin.ModelAdmin):
    list_display = ('inte_cho','point','help_message','require_status','status')
    list_filter = ('inte_cho','status',)
admin.site.register(interview_base,interview_baseAdmin)
#admin.site.register(interview)
#admin.site.register(appointment)
class appointment_userAdmin(admin.ModelAdmin):
    list_display=('cuser','address','contact_person','contact_phone')
    def get_queryset(self, request):
        qs = super(appointment_userAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
           qs=qs.filter(cuser=request.user) 
        return qs
    def save_model(self, request, obj, form, change):
        obj.cuser = request.user
        obj.save()
admin.site.register(appointment_user,appointment_userAdmin)

class appointmentResource(resources.ModelResource):
    name=fields.Field()
    update_date=fields.Field()
    class Meta:
        model = appointment
        fields=('id','cuser__username','app_user__name','app_user__position__name','app_user__provience_applied__name','inte_cho__name','app_date','contact__contact_person',
                'contact__contact_phone','contact__address','check_in','remark',)
        export_order=('id','cuser__username','name','app_user__name','app_user__provience_applied__name','inte_cho__name','app_date','contact__contact_person',
                'contact__contact_phone','contact__address','check_in','remark','update_date',)
    def get_export_headers(self):
        return ['序号','约面人用户名','约面人姓名','应聘者姓名','意向分校','面试类型','面试时间','联系人','联系电话','联系地址','是否参加面试','备注','约面发起时间']
    def dehydrate_name(self,obj):
        name=''
        try:
            name=obj.cuser.last_name+obj.cuser.first_name
        except:
            name='该用户未登记姓名'
        return name
    def dehydrate_update_date(self,obj):
        return obj.update_date.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M")
class appointmentAdmin(ImportExportActionModelAdmin):
    list_display=('cuser','show_name','app_user','show_phone_num','show_provience','show_position','inte_cho','app_date','contact','check_in','update_date',)
    list_filter=('inte_cho','check_in','app_date','app_user__provience_applied','app_user__position','app_date',)
    resource_class=appointmentResource
    def show_name(self,obj):
        name=''
        try:
            name=obj.cuser.last_name+obj.cuser.first_name
        except:
            name='该用户未登记姓名'
        return name
    show_name.short_description='约面人姓名'
    def show_provience(self,obj):
        return obj.app_user.provience_applied
    show_provience.short_description='投递分校'
    def show_position(self,obj):
        return obj.app_user.position
    show_position.short_description='投递岗位'
    def show_phone_num(self,obj):
        return obj.app_user.phone_num
    show_phone_num.short_description='手机号'
    def get_queryset(self, request):
        qs = super(appointmentAdmin, self).get_queryset(request)
#         if not request.user.is_superuser:
#            qs=qs.filter(cuser=request.user) 
#         return qs
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
                qs=qs.filter(app_user__provience_applied__in=p_list)
            else:
                qs=qs.filter(app_user__provience_applied=mp)
            if len(md)>1:
                for i in range(0,len(md)):
                    d_list.append(md[i]['admin_authority_dep'])
                qs=qs.filter(app_user__position__dep__in=d_list)
            else:
               qs=qs.filter(app_user__position__dep__in=md)
            return qs
    def save_model(self, request, obj, form, change):
        obj.cuser = request.user
        obj.save()
admin.site.register(appointment,appointmentAdmin)
admin.site.register(mail_template)
admin.site.register(other_mail_template)
admin.site.register(contract)