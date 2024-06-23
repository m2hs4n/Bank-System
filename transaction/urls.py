from django.urls import path

from transaction import views

urlpatterns = [
    path('', views.TransactionView.as_view(), name='transaction'),
    path('lists/', views.TransactionListView.as_view(), name='transaction-list'),
]
