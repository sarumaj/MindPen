from django import forms
from .models import DataMood


class MoodModelForm(forms.ModelForm):
    class Meta:
        MOOD_TYPES = [
            (1, " Great 😀"),
            (2, " Average 😐"),
            (3, " Upset 😠"),
            (4, " Shocked 😨"),
            (5, " Sad😟"),
        ]
        model = DataMood
        fields = ["mood_score"]
        widgets = {"mood_score": forms.RadioSelect(choices=MOOD_TYPES)}
