from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^process/$',views.show_process,name='show_process'),
    url(r'^getPoints/(?P<cho>[0-9]+)/$',views.getPoints,name='getPoints'),
    url(r'^getHelpMessage/(?P<point>[0-9]+)/$',views.getHelpMessage,name='getHelpMessage'),
]