from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop_index, name='shop_index'),
    path('shop/create/', views.shop_create, name='shop_create'),
    path('shop/update/<int:pk>/', views.shop_edit, name='shop_edit'),
]