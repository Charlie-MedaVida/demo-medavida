from datetime import date

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML as WeasyHTML
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


def _credential_row(label, source, credential):
    if credential is None:
        return None
    status = (
        getattr(credential, '_verification_status', None)
        or 'pending'
    )
    return {
        'label': label,
        'source': source,
        'license_number': credential.license_number or '—',
        'expiration_date': credential.expiration_date,
        'status': status,
    }


def _provider_entry(provider):
    statuses = [
        s for s in (
            provider.npi_verification_status,
            provider.dea_verification_status,
        ) if s is not None
    ]
    if not statuses:
        overall = None
    elif all(s == 'verified' for s in statuses):
        overall = 'verified'
    elif any(s == 'failed' for s in statuses):
        overall = 'failed'
    else:
        overall = 'running'

    verified_creds = sum(1 for s in statuses if s == 'verified')
    total_creds = max(len(statuses), 1)
    pct = round(verified_creds / total_creds * 100)

    credentials = []
    if provider.npi_credential:
        npi = provider.npi_credential
        npi._verification_status = provider.npi_verification_status
        credentials.append(
            _credential_row('NPI', 'NPPES', npi)
        )
    if provider.dea_credential:
        dea = provider.dea_credential
        dea._verification_status = provider.dea_verification_status
        credentials.append(
            _credential_row('DEA License', 'DEA Database', dea)
        )

    first = provider.first_name[0].upper() if provider.first_name else ''
    last = provider.last_name[0].upper() if provider.last_name else ''

    return {
        'first_name': provider.first_name,
        'last_name': provider.last_name,
        'title': provider.title,
        'specialty': provider.specialty,
        'overall_status': overall,
        'completion_pct': pct,
        'credentials': credentials,
        'initials': f'{first}{last}',
    }


class PracticeReportView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, practice_id):
        practice = get_object_or_404(Practice, pk=practice_id)
        providers = Provider.objects.filter(
            provider_practices__practice=practice,
        ).select_related('npi_credential', 'dea_credential')

        provider_entries = [_provider_entry(p) for p in providers]

        total = len(provider_entries)
        verified_count = sum(
            1 for e in provider_entries if e['overall_status'] == 'verified'
        )
        in_progress_count = sum(
            1 for e in provider_entries if e['overall_status'] == 'running'
        )
        pending_count = sum(
            1 for e in provider_entries if e['overall_status'] is None
        )

        today = date.today()
        report_id = (
            f'VV-{today.strftime("%Y-%m%d")}-{str(practice.id)[:4].upper()}'
        )
        context = {
            'practice': practice,
            'providers': provider_entries,
            'total_providers': total,
            'verified_count': verified_count,
            'in_progress_count': in_progress_count,
            'pending_count': pending_count,
            'generated_date': today.strftime('%B %d, %Y'),
            'report_id': report_id,
        }

        html_string = render_to_string(
            'practices/verification_report.html', context, request=request,
        )
        pdf_bytes = WeasyHTML(string=html_string).write_pdf()

        filename = f'verification-report-{practice.id}.pdf'
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


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
