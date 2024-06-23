from rest_framework import serializers

from django.db.models import Q

from card.models import Card

from transaction.models import Transaction


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
