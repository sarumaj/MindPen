from django.shortcuts import render
from .forms import MoodModelForm
from django.http import HttpResponse


def mood(request):
    mood_form = MoodModelForm(initial={"mood_score": 1})
    if request.method == "POST":
        mood_form = MoodModelForm(request.POST)
        if mood_form.is_valid():
            my_mood = mood_form.save(commit=False)
            my_mood.user = request.user
            my_mood.save()
            return HttpResponse("Thank you for submitting your mood.")

    return render(request, "MyMood/mood.html", {"mood_form": mood_form})
