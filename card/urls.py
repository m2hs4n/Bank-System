from django.urls import path

from card import views

urlpatterns = [
    path('verify/<str:card_number>/', views.CardVerifyView.as_view(), name='verify'),
    path('my-cards/', views.MyCardView.as_view(), name='my-cards'),
    path('my-cards/<int:card_id>/', views.MyCardUpdateView.as_view(), name='my-card-update'),
]