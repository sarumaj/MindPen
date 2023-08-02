from django import forms
from .models import Endeavor


class EndeavorModelForm(forms.ModelForm):
    class Meta:
        model = Endeavor
        fields = ["program_title", "start_day", "duration"]


class MultipleTaskForms(forms.Form):
    number = forms.IntegerField(min_value=1, max_value=5)
