from django import forms
from .models import Journal

# render on Journaling webpage
class JournalModelForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"size": "40"}),
            "content": forms.Textarea(attrs={'rows': 4, 'cols': 90})
        }


# render on Dashbord
class JournalModelForm_2(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"size": "30"}),
            "content": forms.Textarea(attrs={'rows': 4, 'cols': 70})
        }

