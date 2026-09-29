from django import forms
from .models import Website


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'domain']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., My Blog',
            }),
            'domain': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
        }
        labels = {
            'name': 'Website Name',
            'domain': 'Website URL',
        }

    def clean_domain(self):
        domain = self.cleaned_data.get('domain', '').strip()
        if not domain.startswith(('http://', 'https://')):
            domain = 'https://' + domain
        return domain