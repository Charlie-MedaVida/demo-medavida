from django import forms

from .models import ReportRequestProxy


class ReportRequestAddForm(forms.ModelForm):
    class Meta:
        model = ReportRequestProxy
        fields = [
            'first_name',
            'last_name',
            'city',
            'state',
            'postal_code',
        ]


class ReportRequestChangeForm(forms.ModelForm):
    class Meta:
        model = ReportRequestProxy
        fields = ['user', 'status']
        widgets = {
            'status': forms.Select(
                choices=ReportRequestProxy.StatusChoices.choices
            ),
        }
