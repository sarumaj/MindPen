from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView

from .forms import MoodForm


# @login_required()
# def mood(request):
#     return render(request, "MyMood/mood.html")


class MoodFromView(View):
    template_name = "MyMood/mood.html"

    def get(self, request, *args, **kwargs):
        mood_form = MoodForm()
        return render(request, self.template_name, {"mood_form": mood_form})

    def post(self, request, *args, **kwargs):
        mood_form = MoodForm(request.POST)
        if mood_form.is_valid():
            mood_form.save()
        return render(request, self.template_name, {"mood_form": mood_form})