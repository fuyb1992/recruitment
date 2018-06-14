from django.contrib import admin
from .forms import *
from .models import *
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from pytz import timezone
from jobs import settings
settings_time_zone = timezone(settings.TIME_ZONE)
# Register your models here.
def get_choices_values(obj,choices):
    for cho in choices:
        if cho[0]==obj:
            return cho[1]
admin.site.register(position_category)
class positionsResource(resources.ModelResource):
    get_dep=fields.Field()
    get_pro = fields.Field()
    get_property=fields.Field()
    update_date=fields.Field()
    class Meta:
        model = positions
        fields=('id','name','position_requirements','position_statement','position_annual_salay_up',
                'position_annual_salay_down','position_monthly_salary_up','position_monthly_salary_down','recruiting_numbers',
                'category__name','sort_value','post_status',)
        export_order= (
        'id', 'name', 'get_dep', 'get_pro', 'position_requirements', 'position_statement', 'position_annual_salay_up',
        'position_annual_salay_down', 'position_monthly_salary_up', 'position_monthly_salary_down',
        'recruiting_numbers',
        'category__name', 'get_property', 'sort_value', 'post_status', 'update_date',)
    def dehydrate_get_dep(self,obj):
        return ','.join([o.name for o in obj.dep.all()])
    def dehydrate_get_pro(self,obj):
        return ','.join([o.name for o in obj.pro.all()])
    def get_export_headers(self):
        return ['序号','岗位名称','招聘部门','招聘分校','岗位要求','岗位描述','年薪上限','年薪下限','月薪上限','月薪下限','招聘人数','岗位类别','岗位性质',
                '排序权重','是否发布','更新日期']
    def dehydrate_get_property(self,obj):
        return get_choices_values(obj.property,pos_choice)
    def dehydrate_update_date(self,obj):
        return obj.update_date.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M")
class positionsAdmin(ImportExportActionModelAdmin):
    resource_class = positionsResource
    form=positionsForm
    list_display = ('name','getdep','getpro','recruiting_numbers','post_status','update_date',)
    list_filter = ('dep','pro',)
admin.site.register(positions,positionsAdmin)