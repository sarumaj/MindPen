from django import forms
from .models import Journal


class JournalModelForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content"]
        widgets = {"content": forms.Textarea(attrs={'rows': 3, 'cols': 60})}

