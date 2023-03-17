# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from dashboard import views
 

app_name = 'dashboard'

urlpatterns = [
    
    
    # The home page
    path('', views.index, name='home'),
    path('',include('dashboard.tables.shop.urls')),
    path('',include('dashboard.tables.actual_purchase.urls')),
    path('',include('dashboard.tables.good.urls')),
    path('',include('dashboard.tables.purchase_history.urls')),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'), 

]
