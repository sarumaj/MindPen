from django import forms
from .models import Journal


class JournalModelForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"size": "40"}),
            "content": forms.Textarea(attrs={'rows': 4, 'cols': 90})
        }

