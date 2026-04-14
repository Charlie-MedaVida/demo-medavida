from django import forms

from vida_verified.models import ReportResults, ReportRequest


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
            'status': forms.Select(
                choices=ReportRequest.StatusChoices.choices
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class ReportChangeForm(forms.ModelForm):
    class Meta:
        model = ReportResults
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
