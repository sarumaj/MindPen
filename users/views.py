from django.shortcuts import render, redirect

# from MyMood.models import DataMood
from Journaling.forms import JournalModelForm_2, JournalModelForm
from .form import LoginForm
from django.views.generic.base import TemplateView

# from SMS.views import send_verification_code
from django.contrib import messages
from Quote.views import get_quote
from Habit_Tracker.views import journaling_frequency
from django.contrib.auth.views import LogoutView
from django.utils.timezone import now


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"

    def dispatch(self, request, *args, **kwargs):
        #  add the logout time to the logged-in user
        if request.user.is_authenticated:
            request.user.last_logout = now()
            request.user.save()
        return super().dispatch(request, *args, **kwargs)


def register(request):
    """
    - Handles user registration including SMS verification
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"{form.cleaned_data['username']}'s account is created successfully!",
            )
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

        # User's last visit
        last_login = self.request.user.last_login
        last_logout = self.request.user.last_logout

        if last_logout is not None:
            time_away = last_login - last_logout
            days_diff = time_away.days
            context["days_diff"] = days_diff
            context["new_user"] = None  # No message for returning users
        else:
            context["days_diff"] = None  # No days difference available
            context["new_user"] = "This is your first visit 🌱"

        return context

    def post(self, request, *args, **kwargs):
        # create a journal entry and associate it with the current user
        journal_form = JournalModelForm_2(request.POST)
        if journal_form.is_valid():
            journal = journal_form.save(commit=False)
            journal.author = self.request.user
            journal.save()
            return redirect("/profile/")
        # last_mood = DataMood.objects.first()

        return render(request, self.template_name, {"form": journal_form})
