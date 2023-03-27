# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from . import views
 

app_name = 'monitoring'

urlpatterns = [
    
    
    # The home page
    path('monitoring/server1', views.server1, name='server1'),
    # path('welcome', views.welcome, name='welcome'),
    # path('', views.welcome, name='welcome'),
    # path('',include('dashboard.tables.shop.urls')),
    # path('',include('dashboard.tables.actual_purchase.urls')),
    # path('',include('dashboard.tables.product.urls')),
    # path('',include('dashboard.tables.purchase_history.urls')),

    # Matches any html file

]
