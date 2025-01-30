from django.contrib import messages
from django.shortcuts import render, redirect
from MyMood.forms import MoodModelForm
from MyMood.models import DataMood
from Journaling.forms import JournalModelForm_2, JournalModelForm
from .form import LoginForm
from django.views.generic.base import TemplateView
from django.utils import timezone
from SMS.views import send_verification_code
from Quote.views import get_quote
from Habit_Tracker.views import journaling_frequency



def register(request):
    """
            - Handles user registration including SMS verification
    """

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            phone_number = form.cleaned_data["phone_number"]

            # send the verification code
            send_verification_code(phone_number)

            # session to save user details temporarily
            request.session["phone_number"] = phone_number
            request.session["user_info"] = form.cleaned_data

            # render a verification page
            return render(request, "users/verification.html")

    else:
        form = LoginForm()
    return render(request, "users/register.html", {"form": form})


class ProfileTemplateViews(TemplateView):
    """
        - Django view for the user profile page
    """
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):

        # initialize a form for journal entries with initial data
        context = super().get_context_data(**kwargs)
        context["form_2"] = JournalModelForm_2()
        context["form"] = JournalModelForm()
        context["quote"] = get_quote()
        context["journaling_percentage"] = journaling_frequency(self.request.user)
        # user's last visit
        last_login = self.request.user.last_login
        if last_login:
            time_diff = timezone.now() - last_login
            # number of days
            days_diff = time_diff.days
        context["days_diff"]= days_diff

        # context["SA"] = analyze_last_journal_sentiment(self.request)
        # Add the mood data
        # context["mood"] = mood(self.request)
        # context["mood_form"] = MoodModelForm(initial={"mood_score": "0"})
        # context["list_endeavor"] = Endeavor.objects.filter(author=self.request.user)[:3]
        # context["list_task"] = Task.objects.filter(endeavor__author=self.request.user)[:3]
        # context["list_accomplished"] = AccomplishedGoal.objects.filter(author=self.request.user)[:3]
        return context

    def post(self, request, *args, **kwargs):
        # create a journal entry and associate it with the current user
        journal_form = JournalModelForm_2(request.POST)
        if journal_form.is_valid():
            journal = journal_form.save(commit=False)
            journal.author = self.request.user
            journal.save()
            return redirect("/profile/")
        last_mood = DataMood.objects.first()

        # create a mood score and associate it with the current user
        # time = timezone.now()
        # mood_form = MoodModelForm(request.POST)
        # if mood_form.is_valid():
        #     my_mood = mood_form.save(commit=False)
        #     my_mood.user = request.user
        #     my_mood.save()
        #     messages.success(request, "Mood recorded🎉 Keep tracking your emotions🚀")
        #     # capture the last mood score
        #     if last_mood and last_mood.mood_date == my_mood.mood_date:
        #         last_mood.delete()
        #     return redirect("/profile/")

        return render(request, self.template_name, {"form": journal_form})


