from django.urls import path, re_path, include
from dashboard import views
 

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome', views.welcome, name='welcome'),
    path('profile', views.profile_index, name='profile_index'),
    path('', views.welcome, name='welcome'),
    path('',include('dashboard.tables.shop.urls')),
    path('',include('dashboard.tables.actual_purchase.urls')),
    path('',include('dashboard.tables.product.urls')),
    path('',include('dashboard.tables.purchase_history.urls')),
    
    path('pages', views.pages, name='pages'), 
]
