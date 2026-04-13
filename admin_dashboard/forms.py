from django import forms

from .models import ReportRequestProxy


class ReportRequestAdminForm(forms.ModelForm):
    class Meta:
        model = ReportRequestProxy
        fields = ['user', 'status']
        widgets = {
            'status': forms.Select(choices=ReportRequestProxy.StatusChoices.choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.instance and self.instance.pk):
            self.fields.pop('user')
            self.fields.pop('status')
            self.fields['first_name'] = forms.CharField(max_length=150, required=False)
            self.fields['last_name'] = forms.CharField(max_length=150, required=False)
            self.fields['city'] = forms.CharField(max_length=100, required=False)
            self.fields['state'] = forms.CharField(max_length=100, required=False)
            self.fields['postal_code'] = forms.CharField(max_length=20, required=False)
