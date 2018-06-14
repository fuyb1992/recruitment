"""jobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import settings
from django.conf.urls.static import static
from . import views
from cv.views import partpdf,interviewpdf
urlpatterns = [
    url(r'^admin/cv/base_info/partpdf/(?P<id>[0-9]+)/$',partpdf,name='partpdf'),
    url(r'^admin/cv/base_info/interviewpdf/(?P<id>[0-9]+)/$',interviewpdf,name='interviewpdf'),
    url(r'^admin/', admin.site.urls),
    url(r'^duals/',include('duals.urls',namespace='duals')),
    url(r'^accounts/',include('accounts.urls',namespace='accounts')),
    url(r'^post/',include('post.urls',namespace='post')),
    url(r'^cv/',include('cv.urls',namespace='cv')),
    url(r'^interview/',include('interview.urls',namespace='interview')),
    url(r'^schools-autocomplete/$',views.schoolsAutocomplete.as_view(),name='schools-autocomplete'),
    url(r'^position_category-autocomplete/$',views.position_categoryAutocomplete.as_view(),name='position_category-autocomplete'),
]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)#This is not suitable for production use!
admin.site.site_header = '招聘系统后台管理'