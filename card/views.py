from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from card.models import Card
from card import serializers


class CardVerifyView(APIView):
    def get(self, request, card_number, *args, **kwargs):
        card = get_object_or_404(Card.objects.select_related("profile_rel"), card_number=card_number)
        serializer = serializers.CardVerifySerializer(instance=card.profile_rel)
        return Response(serializer.data, status.HTTP_200_OK)
