from django import forms
from .models import Endeavor


class EndeavorModelForm(forms.ModelForm):
    class Meta:
        model = Endeavor
        fields = ["program_title", "start_day", "duration"]