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

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user_rel=request.user)
        serializer = serializers.MyCardCreateUpdateDeleteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile_rel=profile)
            return Response(data={"message": "Saved Card successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyCardUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, card_id, *args, **kwargs):
        my_card = get_object_or_404(MyCard, id=card_id)
        serializer = serializers.MyCardCreateUpdateDeleteSerializer(instance=my_card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "Update Card successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, card_id, *args, **kwargs):
        my_card = get_object_or_404(MyCard, id=card_id)
        my_card.delete()
        return Response(data={"message": "Delete Card successfully"}, status=status.HTTP_200_OK)


class CardSendView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, card_id, *args, **kwargs):
        my_card = get_object_or_404(MyCard, id=card_id)
        phone_number_serializer = serializers.MyCardSendPhoneNumberSerializer(data=request.data)
        if phone_number_serializer.is_valid():
            # Send here with sending cloud provider
            return Response(data={"message": f"Send this card number {my_card.card_number} to this phone number {phone_number_serializer.phone_number}"}, status=status.HTTP_200_OK)
        return Response(phone_number_serializer.errors, status=status.HTTP_400_BAD_REQUEST)