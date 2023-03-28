# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from . import views
 

app_name = 'monitoring'

urlpatterns = [
    path('monitoring/server1', views.server1, name='server1'),
    path('api/monitoring/', views.apiServerData, name='api-monitoring'),
    path('api/monitoring/start_record/', views.apiStartRecord, name='api-monitoring'),
]