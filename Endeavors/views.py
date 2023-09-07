from django.shortcuts import render, redirect
from To_Do.models import Task
from .forms import EndeavorModelForm, MultipleTaskForms
from django.forms import formset_factory
from To_Do.forms import TaskModelForm1
from .models import Endeavor
from django.views.generic import (ListView, DeleteView, DetailView)
from django.utils import timezone


def add_endeavor(request):
    current_date = timezone.now()
    multiple_form = MultipleTaskForms()
    if request.method == "POST":
        just_prog_form = EndeavorModelForm(request.POST)
        if just_prog_form.is_valid():
            prog_form = just_prog_form.save(commit=False)
            # check whether that goal title exists
            if Endeavor.objects.filter(author=request.user, title=prog_form.title):
                # display a message
                return render(request, "Endeavors/endeavor_note.html", {"prog_form": prog_form})
            else:
                prog_form.author = request.user
                prog_form.save()
        return render(request, "Endeavors/endeavor_tasks.html", {"just_prog_form": just_prog_form,
                                                                 "multiple_form": multiple_form})
    else:
        just_prog_form = EndeavorModelForm(initial={"start_date": current_date})
    return render(request, "Endeavors/endeavor_tasks.html", {"just_prog_form": just_prog_form})


def tasks(request):
    number_of_tasks = 1
    program = Endeavor.objects.last()
    filled_multiple_tasks_form = MultipleTaskForms(request.GET)
    if filled_multiple_tasks_form.is_valid():
        number_of_tasks = filled_multiple_tasks_form.cleaned_data["number_of_tasks"]
    TaskFormSet = formset_factory(TaskModelForm1, extra=number_of_tasks)
    formset = TaskFormSet()
    if request.method == "POST":
        filled_formset = TaskFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                task = form.save(commit=False)
                task.endeavor = program
                task.save()
            return redirect("list_endeavor")
    else:
        return render(request, "Endeavors/tasks.html", {"formset": formset})
    return render(request, "Endeavors/tasks.html", {"formset": formset})


class ListEndeavorView(ListView):
    model = Endeavor
    template_name = "Endeavors/list_endeavor.html"
    context_object_name = "goals"
    ordering = ["-pk"]

    def get_queryset(self):
        return Endeavor.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        form1 = EndeavorModelForm()
        multiple_form = MultipleTaskForms()
        context = super().get_context_data(**kwargs)
        context["form"] = form1
        context["multiple_form"] = multiple_form
        return context


class DeleteEndeavorView(DeleteView):
    model = Endeavor
    template_name = "Endeavors/delete_endeavor.html"
    success_url = "/list_endeavor/"


class DetailEndeavorView(DetailView):
    model = Endeavor
    template_name = "Endeavors/detail_endeavor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = self.get_object()
        context["tasks"] = Task.objects.filter(endeavor=program)
        return context
