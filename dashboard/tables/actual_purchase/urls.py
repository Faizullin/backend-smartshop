from django.urls import path
from . import views

urlpatterns = [
    path('actual_pururchase',views.PurchaseListView.as_view(), name='actual_purchase_index'),
    path('actual_pururchase/create', views.actual_purchase_create, name='actual_purchase_create'),
    path('actual_pururchase/update/<int:pk>', views.actual_purchase_create, name='actual_purchase_edit'),
    path('actual_pururchase/delete/<int:pk>', views.actual_purchase_delete, name='actual_purchase_delete'),
]
