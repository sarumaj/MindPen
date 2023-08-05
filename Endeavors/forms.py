from django import forms
from .models import Endeavor


class DateInput(forms.DateInput):
    input_type = 'date'


class EndeavorModelForm(forms.ModelForm):
    class Meta:
        model = Endeavor
        fields = ["title", "start_date"]
        widgets = {
            'start_date': DateInput(),
        }


class MultipleTaskForms(forms.Form):
    number_of_tasks = forms.IntegerField(min_value=1, max_value=5)
