from django.urls import path

from card import views

urlpatterns = [
    path('verify/<str:card_number>/', views.CardVerifyView.as_view(), name='verify'),
]