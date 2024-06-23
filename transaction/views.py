from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction

from card.models import Card
from transaction import serializers
from transaction.models import Transaction


class TransactionListView(generics.ListAPIView):
    serializer_class = serializers.TransactionListDetailSerializer
    queryset = Transaction.objects.all()


class TransactionDetailView(APIView):
    def get(self, request, transaction_number,  *args, **kwargs):
        trans = get_object_or_404(Transaction, transaction_number=transaction_number)
        serializer = serializers.TransactionListDetailSerializer(instance=trans)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TransactionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    sender = Card.objects.get(card_number=serializer.data['sender'])
                    receiver = Card.objects.get(card_number=serializer.data['receiver'])
                    sender.stock -= serializer.data['amount']
                    receiver.stock += serializer.data['amount']
                    trans = Transaction(sender=sender, receiver=receiver, amount=serializer.data['amount'])
                    trans.save()
                    sender.save()
                    receiver.save()
                    return Response(data={"message": "transaction successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
