from django import forms
from .models import Hackathon
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.bootstrap import Field


class HackathonForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        fields = ['display_name', 'description', 'theme', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(HackathonForm, self).__init__(*args, **kwargs)
        # self.fields['start_date'].widget = forms.DateTimeInput(attrs={
        #     'required': True,
        #     'type': 'text',
        #     'class': 'form-control datetimepicker-input',
        #     'data-target': '#start_datetimepicker',
        #     # 'data-options': '{"format":"Y-m-d H:i", "timepicker":"true"}'
        # })
        self.fields['end_date'].widget = forms.DateTimeInput(attrs={
            'required': True,
            'class': 'datetimepicker',
            # 'data-options': '{"format":"Y-m-d H:i", "timepicker":"true"}'
        })
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field(
                'start_date',
                field_template='hackathon/includes/datetimefield.html',
                data_date_format="dd MM yyyy - HH:ii P"
            )
        )
