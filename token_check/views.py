import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction

from account.models import Profile
from card.models import Card
from token_check.models import Token

from token_check import serializers


class TokenAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile = get_object_or_404(Profile, user_rel=request.user)
        tokens = Token.objects.filter(profile_rel=profile)
        if tokens.exists():
            serializer = serializers.TokenSerializer(instance=tokens, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message": "Doesn't exist token"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = serializers.TokenCreateSerializer(data=request.data)
        if serializer.is_valid():
            profile = get_object_or_404(Profile, user_rel=request.user)
            try:
                with transaction.atomic():
                    if profile.status == "AC":
                        token = Token(profile_rel=profile, **serializer.validated_data)
                        card = get_object_or_404(Card, profile_rel=profile)
                        if card.stock >= serializer.validated_data['stock']:
                            card.stock -= serializer.validated_data['stock']
                            card.save()
                            token.crate()
                            token_serializer = serializers.TokenSerializer(instance=token)
                            return Response(data=token_serializer.data, status=status.HTTP_200_OK)
                        return Response(data={"message": "Don't have enough money"}, status=status.HTTP_400_BAD_REQUEST)
                    return Response(data={"message": "Your profile is not accepted by bank admin"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(data={"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class TokenDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, token_id):
        profile = get_object_or_404(Profile, user=request.user)
        tokens = get_object_or_404(Token, id=token_id, profile_rel=profile)
        tokens.delete()
        return Response(data={"message": "Deleted Successfully"}, status=status.HTTP_200_OK)


class TokenReceiveView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = serializers.TokenReceiveSerializer(data=request.data)
        if serializer.is_valid():
            profile = get_object_or_404(Profile, user_rel=request.user)
            token = get_object_or_404(Token, token=serializer.validated_data['token'])
            try:
                with transaction.atomic():
                    if token:
                        if token.status == "SU":
                            today = datetime.datetime.today()
                            card = get_object_or_404(Card, profile_rel=profile)
                            card.stock += token.stock
                            card.save()
                            token.status = "RE"
                            token.date_received = today
                            token.save()
                            return Response(data={"message": "Token received successfully"}, status=status.HTTP_200_OK)
                        return Response(data={"message": "The token has already been used"}, status=status.HTTP_400_BAD_REQUEST)
                    return Response(data={"message": "Doesn't exist token"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)