from rest_framework import serializers

from account.models import Profile


class CardVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
        )