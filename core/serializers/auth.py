from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


class SignupSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    firstName = serializers.CharField(write_only=True)
    lastName = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'firstName',
            'lastName',
        )


class OrigTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(OrigTokenObtainPairSerializer, cls).get_token(user)
        token['user_id'] = user.id
        return token


class OrigTokenBlockRefreshSerializer(TokenRefreshSerializer):

    def validate(self, data):
        refresh_token = RefreshToken(data["refresh"])
        refresh_token.blacklist()
        return "The User has logged out succesfully"
