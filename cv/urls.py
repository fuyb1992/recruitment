from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView

urlpatterns=[
    url(r'^base_info/$',views.base_info_view,name='base_info_no_para'),
    url(r'^base_info/(?P<id>[0-9]+)/(?P<pro>[0-9]+)/$',views.base_info_view,name='base_info'),
    url(r'^education_info/$',views.education_info_view,name='education_info'),
    url(r'^work_info/$',views.work_info_view,name='work_info'),
]