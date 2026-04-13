from django import forms

from vida_verified.models import Report, ReportRequest


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
        fields = ['user', 'status']
        widgets = {
            'status': forms.Select(
                choices=ReportRequest.StatusChoices.choices
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class ReportChangeForm(forms.ModelForm):
    npi_credential_status = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='NPI Credential Status',
    )
    dcd_credential_status = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='DCD Credential Status',
    )

    class Meta:
        model = Report
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            npi_contents = list(
                self.instance.npicredentialstatus_set
                .values_list('json_content', flat=True)
            )
            dcd_contents = list(
                self.instance.dcdcredentialstatus_set
                .values_list('json_content', flat=True)
            )
            self.fields['npi_credential_status'].initial = (
                '\n'.join(npi_contents)
            )
            self.fields['dcd_credential_status'].initial = (
                '\n'.join(dcd_contents)
            )
        for field in self.fields.values():
            field.disabled = True
