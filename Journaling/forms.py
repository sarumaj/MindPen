from django import forms
from .models import Journal


class JournalModelForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content", "mood"]
        widgets = {"content": forms.Textarea(attrs={'rows': 2, 'cols': 60})}

