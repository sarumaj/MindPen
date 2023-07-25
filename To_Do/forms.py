from .models import Task
from django import forms


class TaskModelForm1(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task_title", "set_time", "completed"]


class TaskModelForm2(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task_title", "set_time", "completed", "endeavor"]
