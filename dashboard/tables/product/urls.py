from django.urls import path
from . import views

urlpatterns = [
    path('product',views.ProductListView.as_view(), name='product_index'),
    path('product/create', views.product_create, name='product_create'),
    path('product/update/<int:pk>', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>', views.product_delete, name='product_delete'),
]