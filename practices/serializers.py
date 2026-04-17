from rest_framework import serializers

from .models import DeaCredential, NpiCredential, Practice, Provider, ProviderByPractice


class NpiCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = NpiCredential
        fields = (
            'id', 'license_number', 'last_checked_at',
            'enumeration_date', 'expiration_date', 'file',
        )
        read_only_fields = ('id',)


class DeaCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeaCredential
        fields = (
            'id', 'license_number', 'last_checked_at',
            'enumeration_date', 'expiration_date', 'file',
        )
        read_only_fields = ('id',)


class ProviderByPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderByPractice
        fields = ('practice', 'type')


class ProviderSerializer(serializers.ModelSerializer):
    provider_practices = ProviderByPracticeSerializer(many=True, read_only=True)
    npi_credential = NpiCredentialSerializer(read_only=True)
    dea_credential = DeaCredentialSerializer(read_only=True)

    class Meta:
        model = Provider
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'title', 'specialty', 'provider_practices',
            'npi_credential', 'dea_credential',
            'requires_npi', 'requires_dea',
        )
        read_only_fields = ('id', 'requires_npi', 'requires_dea')


class PracticeProviderCreateSerializer(serializers.ModelSerializer):
    """
    Used by POST practice/{practice_id}/providers/.
    All provider fields are optional — practice and type are handled
    in perform_create via the URL and optional body field.
    """
    type = serializers.ChoiceField(
        choices=ProviderByPractice.TypeChoices.choices,
        default=ProviderByPractice.TypeChoices.DEFAULT,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Provider
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'title', 'specialty', 'type',
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


class ProviderSummarySerializer(serializers.ModelSerializer):
    """Flat provider representation used when nested inside a Practice."""
    class Meta:
        model = Provider
        fields = (
            'id', 'first_name', 'last_name', 'email',
            'phone_number', 'title', 'specialty',
        )
        read_only_fields = ('id',)


class PracticeSerializer(serializers.ModelSerializer):
    default_providers = serializers.SerializerMethodField()
    medical_director_providers = serializers.SerializerMethodField()

    class Meta:
        model = Practice
        fields = (
            'id', 'name', 'email', 'phone_number', 'tax_id',
            'npi_number', 'default_providers', 'medical_director_providers',
        )
        read_only_fields = ('id',)

    def get_default_providers(self, obj):
        if not obj.provider_practices.exists():
            return []
        providers = Provider.objects.filter(
            provider_practices__practice=obj,
            provider_practices__type=ProviderByPractice.TypeChoices.DEFAULT,
        )
        return ProviderSummarySerializer(providers, many=True).data

    def get_medical_director_providers(self, obj):
        if not obj.provider_practices.exists():
            return []
        providers = Provider.objects.filter(
            provider_practices__practice=obj,
            provider_practices__type=(
                ProviderByPractice.TypeChoices.MEDICAL_DIRECTOR
            ),
        )
        return ProviderSummarySerializer(providers, many=True).data
