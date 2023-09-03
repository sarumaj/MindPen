from .models import Task
from django import forms


class TaskModelForm1(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "starting_time", "completed"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 1}),
            "starting_time": forms.TextInput(attrs={"type": "datetime-local"}),
        }


class TaskModelForm2(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "starting_time", "completed", "endeavor"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 1}),
            "starting_time": forms.TextInput(attrs={"type": "datetime-local"}),
        }
