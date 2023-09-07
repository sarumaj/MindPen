from django import forms
from .models import DataMood


class MoodModelForm(forms.ModelForm):
    MOOD_TYPES = [
        (-5, "Crying😭"),
        (-4, "Sad😢"),
        (-3, "Angry😠"),
        (-2, "Disappointed😔"),
        (-1, "Unhappy😞"),
        (0, "Neutral😐"),
        (1, "Happy🙂"),
        (2, "Very Happy😄"),
        (3, "Joyful😃"),
        (4, "Excited😁"),
        (5, "Ecstatic🌟"),
    ]
    mood_score = forms.ChoiceField(choices=MOOD_TYPES)

    class Meta:
        model = DataMood
        fields = ["mood_score"]
