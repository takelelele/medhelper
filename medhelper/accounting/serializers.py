from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = "User"
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'phone']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            raise serializers.ValidationError("Пользователь не найден")

        refresh_token = RefreshToken.for_user(user)
        return {
            "user": UserSerializer(user).data,
            "refresh_token": refresh_token,
            "access_token": refresh_token.access_token
        }
