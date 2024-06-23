from django.shortcuts import get_object_or_404

from rest_framework import serializers

from account.models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = [
            'updated_at',
            'created_at',
        ]


class UserPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserPhoneNumberSerializer(partial=True)

    class Meta:
        model = Profile
        fields = [
            'province',
            'city',
            'email',
            'user',
        ]

    def save(self):
        user = UserPhoneNumberSerializer(instance=get_object_or_404(User, pk=self.instance.user_rel_id), data=self.validated_data['user'], partial=True)
        if not user.is_valid():
            return serializers.ValidationError(user.errors)
        user.save()
        return super().save()


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    address = serializers.CharField()
    face_image = serializers.ImageField(required=False)
    province = serializers.CharField()
    city = serializers.CharField()
    national_id = serializers.CharField()
    gender = serializers.CharField()
    birth_date = serializers.DateField()

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, value):
        if value['password'] and value['confirm_password'] and value['password'] != value['confirm_password']:
            raise serializers.ValidationError("Password must be matched")
        value.pop('confirm_password')
        return value

    def save(self, **kwargs):
        raise serializers.ValidationError("kir khar")
        print("dakhel")