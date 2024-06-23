from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction

from card.models import Card
from transaction import serializers
from transaction.models import Transaction


class TransactionListView(generics.ListAPIView):
    serializer_class = serializers.TransactionListSerializer
    queryset = Transaction.objects.all()
