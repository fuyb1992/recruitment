from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView

urlpatterns=[
    url(r'^$',views.show_dualmessages,name='show_dualmessages'),
    url(r'^provience=(?P<pro>[0-9]+)/$',views.show_dualmessages_filter,name='show_dualmessages_filter'),
    url(r'^user_dual/$',views.show_userdual,name='show_userdual'),
    url(r'^user_dual/(?P<pk>[0-9]+)/$',views.user_dualUpdate.as_view(),name='user_dualUpdate'),
]