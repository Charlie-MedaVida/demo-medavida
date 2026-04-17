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


class PracticeProviderCreateSerializer(serializers.ModelSerializer):
    """
    Used by the nested POST practice/{practice_id}/providers/ route.
    All fields are optional — practice is injected from the URL.
    """
    class Meta:
        model = Provider
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'title', 'specialty',
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'first_name':   {'required': False, 'default': ''},
            'last_name':    {'required': False, 'default': ''},
            'email':        {'required': False, 'default': ''},
            'phone_number': {'required': False, 'default': ''},
            'title':        {'required': False, 'default': ''},
            'specialty':    {'required': False, 'default': ''},
        }


class PracticeSerializer(serializers.ModelSerializer):
    providers = ProviderSerializer(many=True, read_only=True)

    class Meta:
        model = Practice
        fields = (
            'id', 'name', 'email', 'phone_number', 'tax_id',
            'npi_number', 'providers',
        )
        read_only_fields = ('id',)
