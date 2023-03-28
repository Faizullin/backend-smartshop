from django.urls import path, re_path, include
from django.conf import settings
from . import views
from rest_framework_simplejwt import views as jwt_views


app_name = 'shop_app'

#EXCLUDED_URLS_FOR_MAIN_APP = [settings.STATIC_URL.strip('/'),settings.MEDIA_URL.strip('/'),'api']

urlpatterns = [
    path('api/user', views.AuthProfileView.as_view()),
    path('api/products', views.ProductView.as_view()),
    path('api/products/<int:pk>', views.ProductDetailView.as_view()),
    path('api/filters', views.ProductFiltersView.as_view()),
    path('api/purchases', views.PurchaseView.as_view()),
    path('api/purchase/order', views.PurchaseView.as_view()),
    path('api/purchase/order_by_bot', views.PurchaseOrderByBotView.as_view()),
    path('api/csrf',views.CsrfTokenView.as_view()),
    path('api/token/', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
    path('api/token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),
    #re_path(r'^(?!media|static).*$', views.index, name='main_app'),
    path('', views.index, name='main_app'),
]