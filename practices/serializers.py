from rest_framework import serializers

from .models import Practice, Provider, ProviderByPractice


class ProviderByPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderByPractice
        fields = ('practice', 'type')


class ProviderSerializer(serializers.ModelSerializer):
    provider_practices = ProviderByPracticeSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'title', 'specialty', 'provider_practices',
        )
        read_only_fields = ('id',)


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
        providers = Provider.objects.filter(
            provider_practices__practice=obj,
            provider_practices__type=ProviderByPractice.TypeChoices.DEFAULT,
        )
        return ProviderSummarySerializer(providers, many=True).data

    def get_medical_director_providers(self, obj):
        providers = Provider.objects.filter(
            provider_practices__practice=obj,
            provider_practices__type=(
                ProviderByPractice.TypeChoices.MEDICAL_DIRECTOR
            ),
        )
        return ProviderSummarySerializer(providers, many=True).data
