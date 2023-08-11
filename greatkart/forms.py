from django import forms
from .models import SiteConfiguration


class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = ['shipping_threshold', 'shipping_cost']
