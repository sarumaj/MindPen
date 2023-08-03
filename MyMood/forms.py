from django import forms
from .models import DataMood


class MoodModelForm(forms.ModelForm):
    class Meta:
        MOOD_TYPES = [
            (-5, " 😭 Crying"),
            (-4, " 😢 Sad"),
            (-3, " 😠 Angry"),
            (-2, " 😔 Disappointed"),
            (-1, " 😞 Unhappy"),
            (0,  " 😐 Neutral"),
            (1,  " 🙂 Happy"),
            (2,  " 😄 Very Happy"),
            (3,  " 😃 Joyful"),
            (4,  " 😁 Excited"),
            (5,  " 🌟 Ecstatic"),
        ]
        model = DataMood
        fields = ["mood_score"]
        widgets = {"mood_score": forms.RadioSelect(choices=MOOD_TYPES)}
