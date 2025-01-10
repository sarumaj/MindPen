from django import forms
from .models import Journal


# render on Journaling webpage
class JournalModelForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "size": "30",
                "placeholder": "Type The Journal Title"
            }),
            "content": forms.Textarea(attrs={
                "rows": 4,
                "cols": 70,
                "placeholder": "Type Your Journal"
            }),
        }


# render on Dashbord
class JournalModelForm_2(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "size": "40",
                "placeholder": "Type The Journal Title"
            }),
            "content": forms.Textarea(attrs={
                "rows": 3,
                "cols": 70,
                "placeholder": "The Audio Inputs Will Appear Here"
            }),
        }
