from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^login/$',views.my_login,name='login'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^change_password/$',views.change_pass,name='change_pass'),
    url(r'^forget_password/$',views.forget_password,name='forget_password'),
]