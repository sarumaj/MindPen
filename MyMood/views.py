from django.shortcuts import render, redirect
from .forms import MoodModelForm
from django.utils import timezone
from .models import DataMood


def mood(request):
    last_mood = DataMood.objects.first()
    time = timezone.now()
    mood_form = MoodModelForm(initial={"mood_score": 0})
    if request.method == "POST":
        mood_form = MoodModelForm(request.POST)
        if mood_form.is_valid():
            my_mood = mood_form.save(commit=False)
            my_mood.user = request.user
            my_mood.save()
            # if last_mood and last_mood.mood_date == my_mood.mood_date:
            #     last_mood.delete()
        return redirect("mood_msg")
    return render(request, "MyMood/mood.html", {"mood_form": mood_form, "time": time})


def mood_message(request):
    time = timezone.now()
    return render(request, "MyMood/mood_message.html", {"time": time})
