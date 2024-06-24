from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Profile
from card.models import Card, MyCard
from card import serializers


class CardVerifyView(APIView):
    def get(self, request, card_number, *args, **kwargs):
        card = get_object_or_404(Card.objects.select_related("profile_rel"), card_number=card_number)
        serializer = serializers.CardVerifySerializer(instance=card.profile_rel)
        return Response(serializer.data, status.HTTP_200_OK)


class MyCardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user_rel=request.user)
        cards = MyCard.objects.filter(profile_rel=profile)
        if cards.exists():
            serializer = serializers.MyCardsSerializer(instance=cards, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message": "Not exists card"}, status=status.HTTP_404_NOT_FOUND)
