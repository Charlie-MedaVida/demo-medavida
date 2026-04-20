from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .business_logic import autofill, nppes_search
from .models import Practice, Provider, ProviderByPractice
from .serializers import (
    DeaCertificateUploadSerializer,
    DeaCredentialSerializer,
    NpiCredentialSerializer,
    PracticeProviderCreateSerializer,
    PracticeSerializer,
    ProviderSerializer,
)


class PracticeViewSet(viewsets.ModelViewSet):
    queryset = Practice.objects.prefetch_related(
        'provider_practices__provider'
    ).all()
    serializer_class = PracticeSerializer
    permission_classes = [IsAuthenticated]


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = (
        Provider.objects.prefetch_related('practices').all()
    )
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]


PROVIDER_TITLES = [
    {'id': 0, 'title': 'Uncredentialed', 'summary': 'Uncredentialed Provider'},
    {'id': 1,  'title': 'MD',      'summary': 'Medical Doctor'},
    {'id': 2,  'title': 'DO',   'summary': 'Doctor of Osteopathic Medicine'},
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
    {'id': 16, 'title': 'CRNA', 'summary': 'Certified Registered Nurse Anesthetist'},  # noqa: E501
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
        relationship_type = serializer.validated_data.pop(
            'type', ProviderByPractice.TypeChoices.DEFAULT
        )
        provider = serializer.save()
        ProviderByPractice.objects.create(
            provider=provider,
            practice=practice,
            type=relationship_type,
        )


class NpiCredentialCreateView(generics.CreateAPIView):
    serializer_class = NpiCredentialSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        provider = Provider.objects.get(pk=self.kwargs['provider_id'])
        credential = serializer.save()
        provider.npi_credential = credential
        provider.save()
        autofill(credential.license_number, credential, provider)


class DeaCredentialCreateView(generics.CreateAPIView):
    serializer_class = DeaCredentialSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        provider = Provider.objects.get(pk=self.kwargs['provider_id'])
        credential = serializer.save()
        provider.dea_credential = credential
        provider.save()


class ProviderVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, provider_id):
        from .signals import provider_verify_requested
        provider = Provider.objects.select_related(
            'npi_credential', 'dea_credential',
        ).get(pk=provider_id)
        provider.npi_verification_status = (
            Provider.VerificationStatus.RUNNING
        )
        provider.dea_verification_status = (
            Provider.VerificationStatus.RUNNING
        )
        provider.save()
        provider_verify_requested.send(
            sender=Provider,
            provider=provider,
        )
        return Response(ProviderSerializer(provider).data)


class CurrentPracticeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            practice = request.user.profile.practice
        except AttributeError:
            raise NotFound('No practice associated with this account.')
        if practice is None:
            raise NotFound('No practice associated with this account.')
        return Response(PracticeSerializer(practice).data)


class NppesSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(nppes_search(request.query_params))


class DeaCertificateUploadView(generics.CreateAPIView):
    serializer_class = DeaCertificateUploadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        from simple_dag_orchestrator.dags import run_dea_license_extraction
        provider = Provider.objects.get(pk=self.kwargs['provider_id'])
        credential = serializer.save()
        provider.dea_credential = credential
        provider.save()
        run_dea_license_extraction.delay(str(credential.id))
