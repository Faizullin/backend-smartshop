from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_index, name='product_index'),
    path('product/create', views.product_create, name='product_create'),
    path('product/update/<int:pk>', views.product_edit, name='product_edit'),
]