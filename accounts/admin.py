from django.contrib import admin

# Register your models here.
from .models import *
from .forms import *
admin.site.register(department)
admin.site.register(provience)
class my_authorityAdmin(admin.ModelAdmin):
    form=my_authorityForm
    list_display = ('admin_user','getdep','getpro',)
    list_filter = ('admin_authority_dep','admin_authority_pro',)
    def get_queryset(self, request):
        qs = super(my_authorityAdmin, self).get_queryset(request)
#         if not request.user.is_superuser:
#            qs=qs.filter(cuser=request.user) 
#         return qs
        if request.user.is_superuser:
            return qs
        else:
            ma=my_authority.objects.filter(admin_user=request.user)
            mp=ma.values('admin_authority_pro')
            p_list=[]
            if len(mp)>1:
                for i in range(0,len(mp)):
                    p_list.append(mp[i]['admin_authority_pro'])
                qs=qs.filter(admin_authority_pro__in=p_list)
            else:
                qs=qs.filter(admin_authority_pro=mp)
            return qs
    def save_model(self, request, obj, form, change):
        obj.cuser = request.user
        obj.save()
admin.site.register(my_authority,my_authorityAdmin)