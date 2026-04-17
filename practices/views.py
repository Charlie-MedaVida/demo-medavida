from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


PROVIDER_TITLES = [
    {'id': 1,  'title': 'MD',      'summary': 'Medical Doctor'},
    {'id': 2,  'title': 'DO',      'summary': 'Doctor of Osteopathic Medicine'},
    {'id': 3,  'title': 'NP',      'summary': 'Nurse Practitioner'},
    {'id': 4,  'title': 'PA',      'summary': 'Physician Assistant'},
    {'id': 5,  'title': 'RN',      'summary': 'Registered Nurse'},
    {'id': 6,  'title': 'LPN',     'summary': 'Licensed Practical Nurse'},
    {'id': 7,  'title': 'DDS',     'summary': 'Doctor of Dental Surgery'},
    {'id': 8,  'title': 'DMD',     'summary': 'Doctor of Dental Medicine'},
    {'id': 9,  'title': 'DPM',     'summary': 'Doctor of Podiatric Medicine'},
    {'id': 10, 'title': 'OD',      'summary': 'Doctor of Optometry'},
    {'id': 11, 'title': 'DC',      'summary': 'Doctor of Chiropractic'},
    {'id': 12, 'title': 'PharmD',  'summary': 'Doctor of Pharmacy'},
    {'id': 13, 'title': 'PT',      'summary': 'Physical Therapist'},
    {'id': 14, 'title': 'OT',      'summary': 'Occupational Therapist'},
    {'id': 15, 'title': 'SLP',     'summary': 'Speech-Language Pathologist'},
    {'id': 16, 'title': 'CRNA',    'summary': 'Certified Registered Nurse Anesthetist'},
    {'id': 17, 'title': 'CNM',     'summary': 'Certified Nurse Midwife'},
    {'id': 18, 'title': 'DPT',     'summary': 'Doctor of Physical Therapy'},
    {'id': 19, 'title': 'AuD',     'summary': 'Doctor of Audiology'},
    {'id': 20, 'title': 'PsyD',    'summary': 'Doctor of Psychology'},
]


class ProviderTitleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(PROVIDER_TITLES)


class PracticeProviderCreateView(generics.CreateAPIView):
    serializer_class = PracticeProviderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        practice = Practice.objects.get(pk=self.kwargs['practice_id'])
        serializer.save(practice=practice)
