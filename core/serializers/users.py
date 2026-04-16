from django.contrib.auth.models import User
from rest_framework import serializers

from practices.models import Practice
from ..models.users import Profile
from .api_keys import UserAPIKeySerializer


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = ('id',)
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    practice = PracticeSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('credit_count', 'practice')


class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only=True)
    api_keys = UserAPIKeySerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile',
            'api_keys',
        )
        read_only_fields = ('id', 'username')


class UserDeleteSerializer(serializers.Serializer):

    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Incorrect password.')
        return value
