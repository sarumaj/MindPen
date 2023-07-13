from django.shortcuts import render, redirect
from django.views.generic import (CreateView,
                                  ListView,
                                  DeleteView,
                                  DetailView,
                                  )
from .forms import EndeavorModelForm, TaskModelForm
from .models import Endeavor


class CreateEndeavorView(CreateView):
    model = Endeavor
    form_class = EndeavorModelForm
    template_name = "Endeavors/create_endeavor.html"
    success_url = "/list_endeavor/"


class ListEndeavorView(ListView):
    model = Endeavor
    template_name = "Endeavors/list_endeavor.html"
    context_object_name = "goals"
    ordering = ["-pk"]


class DeleteEndeavorView(DeleteView):
    model = Endeavor
    template_name = "Endeavors/delete_endeavor.html"
    success_url = "/list_endeavor/"


class DetailEndeavorView(DetailView):
    model = Endeavor
    template_name = "Endeavors/detail_endeavor.html"


def endeavor_task_forms(request):
    if request.method == "POST":
        program_form = EndeavorModelForm(request.POST)
        task_form = TaskModelForm(request.POST)
        if program_form.is_valid() and task_form.is_valid():
            program = program_form.save()  # Save the program and get the created object
            task = task_form.save(commit=False)  # Create the task object but don't save it yet
            task.endeavor = program  # Set the program for the task
            task.save()  # Save the task with the program relationship
            return redirect("list_endeavor")
    else:
        program_form = EndeavorModelForm()
        task_form = TaskModelForm()
    context = {
        "program_form": program_form,
        "task_form": task_form
    }
    return render(request, "Endeavors/endeavor_task_forms.html", context)
