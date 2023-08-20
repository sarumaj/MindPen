from django import forms
from .models import DataMood


class MoodModelForm(forms.ModelForm):
    class Meta:
        MOOD_TYPES = [
            (-5, "😭"),
            (-4, "😢"),
            (-3, "😠"),
            (-2, "😔"),
            (-1, "😞"),
            (0,  "😐"),
            (1,  "🙂"),
            (2,  "😄"),
            (3,  "😃"),
            (4,  "😁"),
            (5,  "🌟"),
        ]
        model = DataMood
        fields = ["mood_score"]
        widgets = {"mood_score": forms.RadioSelect(choices=MOOD_TYPES)}