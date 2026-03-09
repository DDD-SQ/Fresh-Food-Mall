#!/user/bin/env python
# -*- coding: utf-8 -*-
from django.urls import re_path

from .views import *

app_name = 'df_user'

urlpatterns = [
    re_path(r'^register/$', register, name="register"),
    re_path(r'^register_handle/$', register_handle, name="register_handle"),
    re_path(r'^register_exist/$', register_exist, name="register_exist"),
    re_path(r'^login/$', login, name="login"),
    re_path(r'^login_handle/$', login_handle, name="login_handle"),
    re_path(r'^info/$', info, name="info"),
    re_path(r'^order/(\d+)$', order, name="order"),
    re_path(r'^site/$', site, name="site"),
    # url(r'^place_order/$', views.place_order),
    re_path(r'^logout/$', logout, name="logout"),
]