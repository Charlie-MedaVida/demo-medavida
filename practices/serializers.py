from rest_framework import serializers

from .models import Practice, Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'title', 'specialty', 'practice',
        )
        read_only_fields = ('id',)


class PracticeSerializer(serializers.ModelSerializer):
    providers = ProviderSerializer(many=True, read_only=True)

    class Meta:
        model = Practice
        fields = (
            'id', 'name', 'email', 'phone_number', 'tax_id',
            'npi_number', 'providers',
        )
        read_only_fields = ('id',)
