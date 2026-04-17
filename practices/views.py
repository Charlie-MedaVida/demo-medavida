from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Practice, Provider
from .serializers import (
    PracticeProviderCreateSerializer,
    PracticeSerializer,
    ProviderSerializer,
)


class PracticeViewSet(viewsets.ModelViewSet):
    queryset = Practice.objects.prefetch_related('providers').all()
    serializer_class = PracticeSerializer
    permission_classes = [IsAuthenticated]


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.select_related('practice').all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]


class PracticeProviderCreateView(generics.CreateAPIView):
    serializer_class = PracticeProviderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        practice = Practice.objects.get(pk=self.kwargs['practice_id'])
        serializer.save(practice=practice)
