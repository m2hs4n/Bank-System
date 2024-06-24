from rest_framework import serializers

from account.models import Profile

from card.models import MyCard


class CardVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
        )


class MyCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCard
        fields = '__all__'


class MyCardCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCard
        fields = (
            'card_number',
            'cvv2',
            'expiration_date',
        )


class MyCardSendPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()