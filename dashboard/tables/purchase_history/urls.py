from django.urls import path
from . import views

urlpatterns = [
    path('purchase_history',views.PurchaseListView.as_view(), name='purchase_history_index'),
    path('purchase_history/create', views.purchase_history_create, name='purchase_history_create'),
    path('purchase_history/update/<int:pk>', views.purchase_history_edit, name='purchase_history_edit'),
    path('purchase_history/delete/<int:pk>', views.purchase_history_delete, name='purchase_history_delete'),
]