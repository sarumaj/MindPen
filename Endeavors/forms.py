from django import forms
from .models import Endeavor, Task


class EndeavorModelForm(forms.ModelForm):
    class Meta:
        model = Endeavor
        fields = ["program_title", "start_day", "duration"]


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task_title", "set_time", "is_done"]
