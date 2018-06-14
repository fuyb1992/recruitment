# urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.show_positions,name='show_positions'),
    url(r'^property=(?P<pro>[a-z]+)$', views.show_positions,name='show_positions'),
    url(r'^category=(?P<cat>[0-9]+)$', views.show_positions,name='show_positions'),
    url(r'^category=(?P<cat>[0-9]+)property=(?P<pro>[a-z]+)$', views.show_positions,name='show_positions'),
    #url(r'^property=(?P<pro>[a-z]+)/category=(?P<cat>[0-9]+)$', views.show_positions,name='show_positions'),
    url(r'^(?P<id>[0-9]+)/$',views.show_proviences,name='show_pro'),
    url(r'^(?P<id>[0-9]+)/(?P<pro>[0-9]+)/$',views.to_cv,name='to_cv'),
]