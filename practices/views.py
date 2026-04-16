from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Practice, Provider
from .serializers import PracticeSerializer, ProviderSerializer


class PracticeViewSet(viewsets.ModelViewSet):
    queryset = Practice.objects.prefetch_related('providers').all()
    serializer_class = PracticeSerializer
    permission_classes = [IsAuthenticated]


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.select_related('practice').all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]
