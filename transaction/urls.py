from django.urls import path

from transaction import views

urlpatterns = [
    path('', views.TransactionView.as_view(), name='transaction'),
    path('lists/', views.TransactionListView.as_view(), name='transaction-list'),
    path('detail/<int:transaction_number>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
]
