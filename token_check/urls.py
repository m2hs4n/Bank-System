from django.urls import path

from token_check import views

urlpatterns = [
    path('', views.TokenAPIView.as_view(), name='token'),
    path('<int:token_id>/', views.TokenDeleteAPIView.as_view(), name='token_delete'),
    path('receive/', views.TokenReceiveView.as_view(), name='token_receive'),
]
