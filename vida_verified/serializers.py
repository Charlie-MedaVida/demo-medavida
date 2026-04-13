from rest_framework import serializers

from .models import ReportRequest


class ReportRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportRequest
        fields = ('id', 'user', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
