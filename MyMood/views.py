from django.shortcuts import render, redirect
from .forms import MoodModelForm
from django.utils import timezone


def mood(request):
    time = timezone.now()
    mood_form = MoodModelForm(initial={"mood_score": 0})
    if request.method == "POST":
        mood_form = MoodModelForm(request.POST)
        if mood_form.is_valid():
            my_mood = mood_form.save(commit=False)
            my_mood.user = request.user
            my_mood.save()
            return redirect("mood_msg")
    return render(request, "MyMood/mood.html", {"mood_form": mood_form, "time": time})


def mood_message(request):
    time = timezone.now()
    return render(request, "MyMood/mood_message.html", {"time": time})
