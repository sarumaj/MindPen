from django.contrib import messages
from django.http import request
from django.shortcuts import render, redirect
from Endeavors.models import Endeavor
from To_Do.models import Task
from MyMood.models import DataMood
from Journaling.forms import JournalModelForm
from .form import LoginForm
from django.views.generic.base import TemplateView
from Accomplished.views import AccomplishedGoal


def register(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{form.cleaned_data['username']}'s account is created successfully !")
            return redirect("login")
    else:
        form = LoginForm()
    return render(request, "users/register.html", {"form": form})


class ProfileTemplateViews(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = JournalModelForm(initial={"content": "Start journaling now! Share your thoughts, experiences,"
                                                               " and memories right here.",
                                                    "title": "Journal Title"})
        context["list_endeavor"] = Endeavor.objects.filter(author=self.request.user)[:3]
        context["list_task"] = Task.objects.filter(goal__author=self.request.user)[:2]
        context["list_accomplished"] = AccomplishedGoal.objects.filter(author=self.request.user)[:3]
        context["mood"] = DataMood.objects.filter(user=self.request.user).first()

        return context

    def post(self, request, *args, **kwargs):
        journal_form = JournalModelForm(request.POST)
        if journal_form.is_valid():
            journal = journal_form.save(commit=False)
            journal.author = self.request.user
            journal.save()
            return redirect("/profile/")
        return render(request, self.template_name, {"form": journal_form})