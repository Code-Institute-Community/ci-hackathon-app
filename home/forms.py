from django import forms

from .models import PartnershipRequest


class PartnershipRequestForm(forms.ModelForm):
    class Meta:
        model = PartnershipRequest
        fields = ['company', 'email', 'phone', 'contact_name', 'description']
