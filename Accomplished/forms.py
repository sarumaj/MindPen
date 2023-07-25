from django import forms
from .models import AccomplishedGoal


class SummaryModelForm(forms.ModelForm):
    class Meta:
        model = AccomplishedGoal
        fields = ["summary"]
