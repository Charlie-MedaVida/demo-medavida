from django.urls import path

from .views import (
    ReportRequestListCreateView,
    ReportRequestRetrieveUpdateDestroyView,
)

app_name = 'vida_verified'

urlpatterns = [
    path(
        'report-requests/',
        ReportRequestListCreateView.as_view(),
        name=ReportRequestListCreateView.name,
    ),
    path(
        'report-requests/<int:pk>/',
        ReportRequestRetrieveUpdateDestroyView.as_view(),
        name=ReportRequestRetrieveUpdateDestroyView.name,
    ),
]
