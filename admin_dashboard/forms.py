from django import forms

from practices.models import Practice, Provider


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
            'title', 'specialty', 'ssn', 'zip_code',
        ]


class ProviderChangeForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'title', 'specialty', 'ssn', 'zip_code',
        ]
