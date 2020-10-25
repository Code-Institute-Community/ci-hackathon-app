from django import forms
from .models import Resource


class ResourceForm(forms.ModelForm):
    """Allows admin to add/edit resources"""

    class Meta:
        model = Resource
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            "name": "Resource's name",
            "link": "URL",
            "description": "Description",
        }
        for field in self.fields:
            self.fields[field].label = labels[field]
        self.fields['description'].widget.attrs['placeholder'] = "Please, provide few sentences about the resource"
