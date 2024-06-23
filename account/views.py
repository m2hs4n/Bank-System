from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view, extend_schema

from account import serializers
from account.models import Profile, User


@extend_schema_view(get=extend_schema(request=serializers.ProfileSerializer))
class ProfileView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        profile = get_object_or_404(Profile, user_rel=request.user)
        srz = serializers.ProfileSerializer(instance=profile)
        return Response(data=srz.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = get_object_or_404(Profile, user_rel=self.request.user)
        serializer = serializers.ProfileUpdateSerializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():
            if profile:
                serializer.save()
                return Response(data={"message": "Updated successfully"}, status=status.HTTP_200_OK)
            return Response(data={"message": "User not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "Data is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = get_object_or_404(Profile, user_rel=self.request.user)
        profile.user_rel.status = "DE"
        profile.user_rel.save()
        return Response(data={"message": "You are in closing account status"}, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(request=serializers.RegisterSerializer))
class RegisterAccountView(APIView):

    def post(self, request):
        user_serializer = serializers.RegisterSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(data={"message": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user = User(
                    phone_number=user_serializer.validated_data.pop('phone_number'),
                    password=user_serializer.validated_data['password'])
                user.set_password(user_serializer.validated_data.pop('password'))
                user.save()

                user_profile = Profile(user_rel=user, **user_serializer.validated_data)
                user_profile.save()
                return Response(data={"message": "You created registered successfully"}, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(data={"message": "This user already exist"}, status=status.HTTP_400_BAD_REQUEST)