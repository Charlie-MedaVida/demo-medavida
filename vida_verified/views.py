from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import DeaCredential, NpiCredential
from .serializers import DeaCredentialSerializer, NpiCredentialSerializer


class NpiCredentialViewSet(viewsets.ModelViewSet):
    queryset = NpiCredential.objects.all()
    serializer_class = NpiCredentialSerializer
    permission_classes = [IsAuthenticated]


class DeaCredentialViewSet(viewsets.ModelViewSet):
    queryset = DeaCredential.objects.all()
    serializer_class = DeaCredentialSerializer
    permission_classes = [IsAuthenticated]
