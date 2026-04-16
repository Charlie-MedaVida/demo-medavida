from django import forms

from practices.models import Practice, Provider
from vida_verified.models import MonitorRequest, MonitorResults, ReportRequest, ReportResults


class ReportRequestAddForm(forms.ModelForm):
    class Meta:
        model = ReportRequest
        fields = [
            'first_name',
            'last_name',
            'city',
            'state',
            'postal_code',
            'ssn',
            'ein',
            'id_type',
        ]

    class Media:
        js = ('admin/js/report_request_form.js',)


class ReportRequestChangeForm(forms.ModelForm):
    class Meta:
        model = ReportRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=ReportRequest.StatusChoices.choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class MonitorRequestAddForm(forms.ModelForm):
    class Meta:
        model = MonitorRequest
        fields = [
            'first_name',
            'last_name',
            'city',
            'state',
            'postal_code',
            'ssn',
            'ein',
            'id_type',
        ]


class MonitorRequestChangeForm(forms.ModelForm):
    class Meta:
        model = MonitorRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=MonitorRequest.StatusChoices.choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class ReportChangeForm(forms.ModelForm):
    class Meta:
        model = ReportResults
        fields = ['sam_exclusions_results', 'npi_registration_results']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class MonitorResultsChangeForm(forms.ModelForm):
    class Meta:
        model = MonitorResults
        fields = ['sam_exclusions_results', 'npi_registration_results']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class PracticeAddForm(forms.ModelForm):
    class Meta:
        model = Practice
        fields = ['name', 'email', 'phone_number', 'tax_id', 'npi_number']


class PracticeChangeForm(forms.ModelForm):
    class Meta:
        model = Practice
        fields = ['name', 'email', 'phone_number', 'tax_id', 'npi_number']


class ProviderAddForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'title', 'specialty', 'practice',
        ]


class ProviderChangeForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'title', 'specialty', 'practice',
        ]
