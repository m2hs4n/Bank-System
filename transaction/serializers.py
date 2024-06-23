from rest_framework import serializers

from django.db.models import Q

from card.models import Card

from transaction.models import Transaction


class TransactionSerializer(serializers.Serializer):
    sender = serializers.CharField()
    receiver = serializers.CharField()
    amount = serializers.IntegerField()

    def validate(self, value):
        if not value["sender"] == value["receiver"]:
            if Card.objects.filter(Q(card_number=value["sender"]) | Q(card_number=value["receiver"])).count() == 2:
                if Card.objects.get(card_number=value["sender"]).stock >= value["amount"]:
                    return value
                raise serializers.ValidationError({"message": "Don't have enough money"})
            raise serializers.ValidationError({"message": "Invalid sender or receiver"})
        raise serializers.ValidationError({"message": "You can't transaction to your self"})


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
