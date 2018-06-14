from django.contrib import admin
 
# Register your models here.
from .models import *
from interview.models import *
from interview.forms import *
#from django.utils.functional import curry
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from accounts.models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError
from smtplib import SMTPException
from django.core.mail import send_mail, EmailMessage
from jobs import settings
from django.core.exceptions import ValidationError
from pytz import timezone
from jobs import settings
settings_time_zone = timezone(settings.TIME_ZONE)
def get_choices_values(obj,choices):
    for cho in choices:
        if cho[0]==obj:
            return cho[1]
class base_infoResource(resources.ModelResource):
    junior=fields.Field()
    bachelor = fields.Field()
    master = fields.Field()
    doctor=fields.Field()
    get_sex=fields.Field()
    get_minzu=fields.Field()
    get_provience=fields.Field()
    get_marital=fields.Field()
    get_politics=fields.Field()
    work=fields.Field()
    update_time=fields.Field()
    get_status=fields.Field()
    class Meta:
        model = base_info
        #exclude = ('photo', 'reject',)
        fields=('id','cuser__username','position__name','provience_applied__name','name','channel',
                'phone_num','cuser__email','id_num','language','language_leve','teacher_cert','address',
                'salary_except','salary_monthly','salary_annual','stage__name',)
        export_order=('id','channel','position__name','provience_applied__name','cuser__username','name','get_sex','get_minzu',
                      'get_provience','get_marital','get_politics','phone_num','cuser__email','id_num','language','language_leve',
                      'teacher_cert','address','junior','bachelor','master','doctor','work','salary_except','salary_monthly',
                      'salary_annual','update_time','stage__name','get_status',)
    def get_export_headers(self):
        return ['序号','渠道','申请岗位','申请分校','用户名','姓名','性别','民族','籍贯','婚姻状况','政治面貌','手机号','邮箱',
                '身份证号','外语语种','外语水平','教师资格证','现居住地','专科','本科','硕士','博士','工作经历','期望薪金',
                '基本月薪','目标年薪','简历投递时间','面试阶段','面试结果']
    def dehydrate_update_time(self,obj):
        return obj.update_time.astimezone(settings_time_zone).strftime("%Y-%m-%d %H:%M")
    def dehydrate_junior(self, obj):
        edu_str=''
        edus=education_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser)).filter(degree='a')
        for edu in edus:
           edu_str+=(str(edu.school)+','+str(edu.school.pc)+','+edu.major+','+edu.start_date.strftime('%Y/%m/%d')+'-'+edu.end_date.strftime('%Y/%m/%d'))
        return edu_str
    def dehydrate_bachelor(self, obj):
        edu_str=''
        edus=education_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser)).filter(degree='b')
        for edu in edus:
           edu_str+=(str(edu.school)+','+str(edu.school.pc)+','+edu.major+','+edu.start_date.strftime('%Y/%m/%d')+'-'+edu.end_date.strftime('%Y/%m/%d'))
        return edu_str
    def dehydrate_master(self,obj):
        edu_str=''
        edus=education_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser)).filter(degree='c')
        for edu in edus:
           edu_str+=(str(edu.school)+','+str(edu.school.pc)+','+edu.major)
        return edu_str
    def dehydrate_doctor(self,obj):
        edu_str=''
        edus=education_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser)).filter(degree='d')
        for edu in edus:
           edu_str+=(str(edu.school)+','+str(edu.school.pc)+','+edu.major)
        return edu_str
    def dehydrate_get_sex(self,obj):
        return get_choices_values(obj.sex,sex_choices)
    def dehydrate_get_minzu(self,obj):
        return get_choices_values(obj.minzu,minzu_choices)
    def dehydrate_get_provience(self,obj):
        return get_choices_values(obj.provience,provience_choices)
    def dehydrate_get_marital(self,obj):
        return get_choices_values(obj.marital_status, marital_choices)
    def dehydrate_get_politics(self,obj):
        return get_choices_values(obj.politics_status, politics_choices)
    def dehydrate_get_status(self,obj):
        return get_choices_values(obj.status, inter_status_choices)
    def dehydrate_work(self,obj):
        work_str=''
        works=work_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser))
        for work in works:
            work_str+=work.company+','+work.position+','+work.start_date.strftime('%Y/%m/%d')+'-'+work.end_date.strftime('%Y/%m/%d')+';'
        return work_str
class education_infoInline(admin.TabularInline):
    model=education_info
    form=education_infoForm
    max_num=3
class work_infoInline(admin.TabularInline):
    model=work_info
    max_num=3
class interviewInline(admin.TabularInline):
    model=interview
    form=interviewInlineForm
class appointmentInline(admin.TabularInline):
    model=appointment
    form=appointmentInlineForm
    max_num=5
class offer_readyInline(admin.TabularInline):
    model=offer_ready
    form=offer_readyInlineForm
    max_num=1
class offer_approvalInline(admin.TabularInline):
    model=offer_approval
    form=offer_approvalInlineForm
    max_num=1
class in_serviceInline(admin.TabularInline):
    model=in_service
    max_num=1
i=0
len_inter=0
inte_mcho=[]
for ic in interview_choices.objects.all():
    inte_mcho.append(ic.name)
    len_inter+=1
req=[[]]*len_inter
for cho in interview_choices.objects.all():
    inter=interview_base.objects.filter(require_status=True).filter(status=True).filter(inte_cho=cho)
    temp=[]
    for inte in inter:
        temp.append(inte.id)
    req[i]=temp
    i+=1
class base_infoAdmin(ImportExportActionModelAdmin):
    resource_class = base_infoResource
    list_display = ('cuser','position','provience_applied','name','sex','get_doctor','get_master','get_bachelor','get_junior','update_time','get_first_interview','get_partpdf','get_interviewpdf','status','get_offer_ready','get_offer_ready_date','get_offer_approval',)
    list_filter = ('stage','status','position','provience_applied',)
    date_hierarchy='update_time'
    actions=['make_offer_ready','make_offer_approval','send_rejection_letter']
    search_fields=['name','phone_num','id_num']
    inlines = (
        education_infoInline,
        work_infoInline,
        appointmentInline,
        interviewInline,
        offer_readyInline,
        offer_approvalInline,
        in_serviceInline,
    )
    def get_partpdf(self,obj):
        str_display="<a target='_blank'  href='partpdf/%d'>PDF</a>"%obj.id
        return str_display
    get_partpdf.allow_tags=True
    get_partpdf.short_description = "简历"
    def get_interviewpdf(self,obj):
        str_display="<a target='_blank'  href='interviewpdf/%d'>PDF</a>"%obj.id
        return str_display
    get_interviewpdf.allow_tags=True
    get_interviewpdf.short_description = "面试记录"
    def make_offer_ready(self, request, queryset):
        queryset.update(status='4')
        if request.user.has_perm('interview.add_offer_ready') and request.user.has_perm('interview.change_offer_ready'):
            i=0
            j=0
            for obj in queryset:
                try:
                    offer_ready.objects.update_or_create(cuser=request.user,offer_user=obj,ready=True)
                    i+=1
                except IntegrityError:
                    j+=1
            self.message_user(request,'%d条预入职信息提交成功！%d条信息已存在！'%(i,j))
        else:
            self.message_user(request,'权限不足！',level=messages.ERROR)
    make_offer_ready.short_description = "提交预入职"
    def make_offer_approval(self, request, queryset):
        if request.user.has_perm('interview.add_offer_approval') and request.user.has_perm('interview.change_offer_approval'):
            queryset.update(status='5')
            mail_message=other_mail_template.objects.get(mail_cat='发放offer').template_context
            i=0
            j=0
            for obj in queryset:
                try:
                    offer_approval.objects.update_or_create(cuser=request.user,offer_user=obj,approval=True)
                    mail_message=mail_message.replace('{姓名}',str(obj.name)).replace('{岗位名称}',str(obj.position.name)).replace('{月薪}',str(obj.salary_monthly)).replace('{年薪}',str(obj.salary_annual)).replace('{省份}',str(obj.provience_applied))
                    send_mail('中公教育面试结果通知', mail_message, settings.DEFAULT_FROM_EMAIL,[obj.cuser.email], fail_silently=False)
                    i+=1
                except IntegrityError:
                    j+=1
                except SMTPException as e:
                    self.message_user(request,'%s的offer发送失败，请手动补发！错误代码：%s'% (str(obj.name),str(e)),level=messages.WARNING)
                except BaseException as e:
                    self.message_user(request,'%s的信息处理错误，捕捉到未知错误，请联系管理员，错误代码：%s'% (str(obj.name),str(e)),level=messages.ERROR)
            self.message_user(request,'%d条预入职信息审核成功，系统邮件发送成功！%d条信息已存在！'%(i,j))
        else:
            self.message_user(request,'权限不足！',level=messages.ERROR)
    make_offer_approval.short_description = "预入职审核通过"
    def send_rejection_letter(self, request, queryset):
        mail_message=other_mail_template.objects.get(mail_cat='拒信').template_context
        i=0
        for obj in queryset:
            print (obj)
            try:
                mail_message=mail_message.replace('{姓名}',str(obj.name)).replace('{岗位名称}',str(obj.position.name))
                send_mail('中公教育面试结果通知', mail_message, settings.DEFAULT_FROM_EMAIL,[obj.cuser.email], fail_silently=False)
                i+=1
            except:
                self.message_user(request,'%s的系统邮件发送失败，请手动发送！' % obj.name,level=messages.ERROR)
        self.message_user(request,'%d封系统邮件发送成功！'% i)
        queryset.update(status='3')
    send_rejection_letter.short_description = '发送拒信'
    def get_junior(self,obj):
        edu_str=''
        edus=education_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser)).filter(degree='a')
        for edu in edus:
           edu_str+=(str(edu.school)+','+str(edu.school.pc)+','+edu.major)
        return edu_str
    get_junior.short_description='专科'
    def get_bachelor(self,obj):
        edu_str=''
        edus=education_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser)).filter(degree='b')
        for edu in edus:
           edu_str+=(str(edu.school)+','+str(edu.school.pc)+','+edu.major)
        return edu_str
    get_bachelor.short_description='本科'
    def get_master(self,obj):
        edu_str=''
        edus=education_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser)).filter(degree='c')
        for edu in edus:
           edu_str+=(str(edu.school)+','+str(edu.school.pc)+','+edu.major)
        return edu_str
    get_master.short_description='硕士'
    def get_doctor(self,obj):
        edu_str=''
        edus=education_info.objects.filter(name=base_info.objects.get(cuser=obj.cuser)).filter(degree='d')
        for edu in edus:
           edu_str+=(str(edu.school)+','+str(edu.school.pc)+','+edu.major)
        return edu_str
    get_doctor.short_description='博士'
#admin.site.register(base_info,base_infoAdmin)
    def get_first_interview(self,obj):
        apps=appointment.objects.filter(app_user=obj)
        app_str=''
        for app in apps:
            app_str+=str(app.inte_cho)+':'+app.app_date.strftime("%Y-%m-%d %H:%M")+';'
        return app_str
    get_first_interview.short_description='约面'
    def get_offer_ready(self,obj):
        return obj.offer_ready_base_info.ready
    get_offer_ready.boolean = True
    get_offer_ready.short_description='提交预入职'
    def get_offer_ready_date(self,obj):
        return obj.offer_ready_base_info.update_date
    get_offer_ready_date.short_description='提交时间'
    get_offer_ready_date.admin_order_field='offer_ready_base_info__update_date'
    def get_offer_approval(self,obj):
        return obj.offer_approval_base_info.approval
    get_offer_approval.boolean = True
    get_offer_approval.short_description='预入职审核'
 
    def save_formset(self, request, form, formset, change):
        fill=[0]*len_inter
        if formset.model not in [interview,appointment,offer_ready,offer_approval,in_service]:
            return super(base_infoAdmin, self).save_formset(request, form, formset, change)
        if formset.model not in [appointment,interview,in_service]:
            instances=formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    instance.cuser=request.user
                instance.save()
        elif formset.model ==interview:
            instances=formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    #更新base_info模型后两个字段
                    base_info_instance=base_info.objects.get(pk=instance.inter_user.id)
                    base_info_instance.stage=instance.inter_cho
                    base_info_instance.status='2'
                    base_info_instance.save()
                    instance.cuser=request.user
                    instance.position=str(instance.inter_user.provience_applied)+str(instance.inter_user.position)
                    i=0
                    for req_t in req:
                        if instance.point.id in req_t:
                            fill[i]+=1
                        i+=1
                instance.save()
            for ii in range(0,len_inter):
                if fill[ii] and fill[ii]<len(req[ii]):
                    self.message_user(request,'%s的必填面试要点缺失，请检查！' %inte_mcho[ii],level=messages.ERROR)
        elif formset.model==in_service:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.cuser = request.user
                if instance.on_board:
                    in_service_instance = base_info.objects.get(pk=instance.offer_user.id)
                    in_service_instance.status = '6'
                    in_service_instance.save()
                else:
                    in_service_instance = base_info.objects.get(pk=instance.offer_user.id)
                    in_service_instance.status = '7'
                    in_service_instance.save()
                instance.save()
        else:
            instances=formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    base_info_instance=base_info.objects.get(pk=instance.app_user.id)
                    base_info_instance.stage=instance.inte_cho
                    base_info_instance.status='1'
                    base_info_instance.save()
                    instance.cuser=request.user
                    try:
                        mailtempalte=mail_template.objects.get(pos_cat=instance.app_user.position.category)
                        mail_message=mailtempalte.template_context.replace('{姓名}',str(instance.app_user.name)).replace('{面试类型}',str(instance.inte_cho.name)).replace('{时间}',instance.app_date.strftime("%Y-%m-%d %H:%M")).replace('{地址}',str(instance.contact.address)).replace('{联系人}',str(instance.contact.contact_person)).replace('{电话}',str(instance.contact.contact_phone))
                        msg = EmailMessage('中公教育面试邀请', mail_message, settings.DEFAULT_FROM_EMAIL,[request.user.email])
                        msg.content_subtype='html'
                        msg.send()
                        self.message_user(request,'%s的系统邮件发送成功！'%str(instance.app_user.name))
                    except :
                        self.message_user(request,'系统邮件发送失败，请手动发送！',level=messages.ERROR)
                instance.save()
                
        formset.save_m2m()
    def get_queryset(self, request):
        """
        Filter the objects displayed in the change_list
        """
        qs = super(base_infoAdmin, self).get_queryset(request)
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
 
admin.site.register(base_info,base_infoAdmin)
#admin.site.register(education_info)
class in_serviceResource(resources.ModelResource):
    name=fields.Field()
    class Meta:
        model = in_service
        fields = ('id','offer_user__name','offer_user__position__name','offer_user__provience_applied__name','date_predict','contract__name','on_board','date_in',)
        export_order= ('id','offer_user__name','offer_user__position__name','offer_user__provience_applied__name','name','date_predict','contract__name','on_board','date_in',)
    def get_export_headers(self):
        return ['序号', '应聘者姓名', '应聘岗位', '应聘分校', '面试官姓名', '预计入职日期', '合同类型', '实际是否入职', '实际入职日期']

    def dehydrate_name(self, obj):
        name = ''
        try:
            name = obj.cuser.last_name + obj.cuser.first_name
        except:
            name = '该用户未登记姓名'
        return name
class in_serviceAdmin(ImportExportActionModelAdmin):
    resource_class = in_serviceResource
    list_display = (
    'offer_user','show_provience','show_position','show_phone_num','show_name', 'date_predict', 'contract', 'on_board', 'date_in',)
    list_filter = ('contract', 'on_board', 'date_predict','date_in','offer_user__provience_applied','offer_user__position',)
    def show_provience(self,obj):
        return obj.offer_user.provience_applied
    show_provience.short_description='投递分校'
    def show_position(self,obj):
        return obj.offer_user.position
    show_position.short_description='投递岗位'
    def show_phone_num(self,obj):
        return obj.offer_user.phone_num
    show_phone_num.short_description='手机号'
    def show_name(self,obj):
        name=''
        try:
            name=obj.cuser.last_name+obj.cuser.first_name
        except:
            name='该用户未登记姓名'
        return name
    show_name.short_description='面试官姓名'
    def get_queryset(self, request):
        """
        Filter the objects displayed in the change_list
        """
        qs = super(in_serviceAdmin, self).get_queryset(request)
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
                qs=qs.filter(offer_user__provience_applied__in=p_list)
            else:
                qs=qs.filter(offer_user__provience_applied=mp)
            if len(md)>1:
                for i in range(0,len(md)):
                    d_list.append(md[i]['admin_authority_dep'])
                qs=qs.filter(offer_user__position__dep__in=d_list)
            else:
               qs=qs.filter(offer_user__position__dep__in=md)
            return qs
admin.site.register(in_service,in_serviceAdmin)