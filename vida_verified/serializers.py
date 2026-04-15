from rest_framework import serializers

from .models import ReportRequest


class ReportRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportRequest
        fields = (
            'id', 'uuid', 'first_name', 'last_name', 'city', 'state',
            'postal_code', 'ssn', 'ein', 'id_type', 'status',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')
