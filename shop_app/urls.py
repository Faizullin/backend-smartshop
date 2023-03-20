from django.urls import path, re_path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views


app_name = 'shop_app'

urlpatterns = [
    path('api/products', views.ProductView.as_view()),
    path('api/products/<int:id>', views.ProductView.as_view()),
    path('api/filters', views.ProductFiltersView.as_view()),
    path('api/purchases', views.PurchaseView.as_view()),
    path('api/purchases/<int:id>', views.PurchaseView.as_view()),
    path('api/purchase/order', views.PurchaseOrderView.as_view()),
    path('api/purchase/order_by_bot', views.PurchaseOrderByBotView.as_view()),
    path('api/token/', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
    path('api/token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),
    #path('', views.index, name='main_app')
    re_path(r'^.*\.*', views.index, name='main_app'),
]