from django.shortcuts import render, redirect
from MyMood.models import DataMood
from Journaling.forms import JournalModelForm_2, JournalModelForm
from .form import LoginForm
from django.views.generic.base import TemplateView
from django.utils import timezone
# from SMS.views import send_verification_code
from django.contrib import messages
from Quote.views import get_quote
from Habit_Tracker.views import journaling_frequency


def register(request):
    """
            - Handles user registration including SMS verification
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{form.cleaned_data['username']}'s account is created successfully!")
            return redirect("login")
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
            # get number of days
            days_diff = time_diff.days
        context["days_diff"] = days_diff

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

        return render(request, self.template_name, {"form": journal_form})
