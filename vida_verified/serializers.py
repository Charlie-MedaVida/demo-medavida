from rest_framework import serializers

from .models import DeaCredential, NpiCredential


class NpiCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = NpiCredential
        fields = [
            'id',
            'license_number',
            'last_checked_at',
            'enumeration_date',
            'expiration_date',
            'file',
        ]
        read_only_fields = ['id']


class DeaCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeaCredential
        fields = [
            'id',
            'license_number',
            'last_checked_at',
            'enumeration_date',
            'expiration_date',
            'file',
        ]
        read_only_fields = ['id']
