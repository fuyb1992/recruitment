from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
# Register your models here.
from .models import *
from accounts.models import *
from .forms import *
from import_export import resources
from import_export import fields
from jobs import settings
from pytz import timezone
settings_time_zone = timezone(settings.TIME_ZONE)
def get_choices_values(obj,choices):
    for cho in choices:
        if cho[0]==obj:
            return cho[1]
class dualmessagesResource(resources.ModelResource):
    update_time=fields.Field()
    preferred_date=fields.Field()
    post=fields.Field()
    class Meta:
        model = dualmessages
        fields=('id','name','school__name','deadline','provience__name','address','url_adress','cost','person_attend','cv_num','ks','comment',)
        export_order=('id','name','school__name','update_time','deadline','preferred_date','provience__name','address','url_adress','post','cost','person_attend','cv_num','ks','comment',)
    def dehydrate_update_time(self,obj):
        return obj.update_time.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M")
    def dehydrate_preferred_date(self,obj):
        return obj.preferred_date.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M")
    def dehydrate_post(self,obj):
        return get_choices_values(obj.post,status_choices)
    def get_export_headers(self):
        return ['序号', '双选会/渠道名称', '高校', '更新时间', '截止时间', '举办日期', '所在省份', '地址', '链接', '发布状态', '费用', '参加人员姓名', '收到简历数',
                '是否跨省', '备注']
class dualmessagesAdmin(ImportExportActionModelAdmin):
    resource_class=dualmessagesResource
    list_display = ('id','name','school','update_time','deadline','preferred_date','provience','cost','post','person_attend','cv_num','ks',)
    list_filter = ('provience','deadline','preferred_date','ks',)
    form=dualmessagesForm
    def get_queryset(self, request):
        """
        Filter the objects displayed in the change_list
        """
        qs = super(dualmessagesAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            ma=my_authority.objects.filter(admin_user=request.user)
            mp=ma.values('admin_authority_pro')
            p_list=[]
            d_list=[]
            if len(mp)>1:
                for i in range(0,len(mp)):
                    p_list.append(mp[i]['admin_authority_pro'])
                qs=qs.filter(provience__in=p_list)
            else:
                qs=qs.filter(provience=mp)
            return qs
admin.site.register(dualmessages,dualmessagesAdmin)
class schoolsAdmin(ImportExportActionModelAdmin):
    list_display=('id','name','pc',)
    list_filter=('pc',)
    search_fields=['name']
admin.site.register(schools,schoolsAdmin)

# class user_dualAdmin(admin.ModelAdmin):
#     list_display = ('cuser','dual','dual_status','person_attend',)
#     list_filter = ('dual_status',)
# admin.site.register(user_dual,user_dualAdmin)
