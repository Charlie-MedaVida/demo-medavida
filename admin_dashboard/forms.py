from django import forms

from vida_verified.models import ReportRequest


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