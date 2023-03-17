from django.urls import path
from . import views

urlpatterns = [
    path('actual_purchase/', views.actual_purchase_index, name='actual_purchase_index'),
    path('actual_purchase/create', views.actual_purchase_create, name='actual_purchase_create'),
    path('actual_purchase/update/<int:pk>', views.actual_purchase_edit, name='actual_purchase_edit'),
]