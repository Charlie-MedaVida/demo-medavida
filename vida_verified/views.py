from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import ReportRequest
from .serializers import ReportRequestSerializer


class ReportRequestListCreateView(generics.ListCreateAPIView):
    name = 'REPORT_REQUEST_LIST_CREATE'
    serializer_class = ReportRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReportRequest.objects.all()


class ReportRequestRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    name = 'REPORT_REQUEST_RETRIEVE_UPDATE_DESTROY'
    serializer_class = ReportRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReportRequest.objects.all()
