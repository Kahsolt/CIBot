#encoding: utf-8
from django.conf.urls import url
from app import views

# 路由分发层 Router - HTTP
#   函数名尽量与url对应，或者遵守一定的命名约定只要便于管理即可
#   注意url从上到下的匹配顺序
#

urlpatterns = [
    url(r'^user$', views.user),
    url(r'^user/login$', views.user_login),
    url(r'^user/logout$', views.user_logout),
    url(r'^user/register$', views.user_register),
    url(r'^user/keepalive$', views.user_keepalive),
    url(r'^tag$', views.tag),
    url(r'^q$', views.q),
    url(r'^a$', views.a),

    url(r'^log$', views.log),
    url(r'^test$', views.test),
    url(r'^index$', views.index),
    url(r'^$', views.index),
]
