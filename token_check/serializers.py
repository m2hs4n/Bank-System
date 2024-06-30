import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from token_check.models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class TokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        exclude = [
            'profile_rel',
            'token',
            'updated_at',
            'created_at',
        ]


class TokenReceiveSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(allow_null=True)

    def validate(self, attrs):
        today = datetime.date.today()
        token = get_object_or_404(Token, token=attrs['token'])
        if token.date_allow_receipt:
            if token.date_allow_receipt >= today:
                raise serializers.ValidationError("date allow receipt must be in the past")

        if token.expiration_date:
            if token.expiration_date <= today:
                raise serializers.ValidationError("expiration date must be in the future")

        if token.password:
            if not attrs.get('password'):
                raise serializers.ValidationError("password is required token has password")
            if token.password != attrs.get('password'):
                raise serializers.ValidationError("password must match")
        return attrs