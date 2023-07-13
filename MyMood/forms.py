from django import forms


class MoodForm(forms.Form):
    OPTIONS = (
        ("Rich", "I feel rich🤑"), ("Sick", "I feel sick🤒"), ("Angry", "I feel angry😠"),
        ("Cool", "I feel cool😎"), ("Sleepy", "I feel sleepy🥱"), ("Happy", "I feel happy😀"),
        ("Excited", "I feel excited🤠"), ("scared", "I feel sad😢"), ("Neutral", "I feel neutral😐")
    )

    my_mood = forms.ChoiceField(widget=forms.RadioSelect, choices=OPTIONS)
