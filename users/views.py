from django.contrib import messages
from django.shortcuts import render, redirect

from Endeavors.models import Endeavor, Task
from .form import LoginForm
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Journaling.forms import JournalModelForm


def register(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account is successfully created!")
            return redirect("login")
    else:
        form = LoginForm()
    return render(request, "users/register.html", {"form": form})


class ProfileTemplateViews(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JournalModelForm()
        context['list_endeavor'] = list(Endeavor.objects.values_list('program_title', flat=True))
        context['list_task'] = list(Task.objects.values_list('task_title', flat=True))
        return context

    def post(self, request, *args, **kwargs):
        journal_form = JournalModelForm(request.POST)
        if journal_form.is_valid():
            journal = journal_form.save(commit=False)
            journal.user = request.user  # Assuming you have a user field in your Journal model
            journal.save()
            return redirect("profile")
        return render(request, self.template_name, {"form": journal_form})

