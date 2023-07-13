from django import forms
from .models import Journal


class JournalModelForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content"]
