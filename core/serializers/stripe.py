from rest_framework import serializers
from ..models import StripePrice


class StripePriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripePrice
        fields = ('id', 'lookup_key')
