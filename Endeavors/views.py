from django.shortcuts import render, redirect

from To_Do.models import Task
from .forms import EndeavorModelForm, MultipleTaskForms
from django.forms import formset_factory
from To_Do.forms import TaskModelForm1
from .models import Endeavor
from django.views.generic import (CreateView,
                                  ListView,
                                  DeleteView,
                                  DetailView,
                                  )


# class CreateEndeavorView(CreateView):
#     model = Endeavor
#     form_class = EndeavorModelForm
#     template_name = "Endeavors/create_endeavor.html"
#
#     def post(self, request, *args, **kwargs):
#         form = EndeavorModelForm(request.POST)
#         if form.is_valid():
#             form_endeavor = form.save(commit=False)
#             form_endeavor.author = self.request.user
#             form_endeavor.save()
#             return redirect("list_endeavor")

def add_endeavor(request):
    multiple_form = MultipleTaskForms()
    if request.method == "POST":
        just_prog_form = EndeavorModelForm(request.POST)
        if just_prog_form.is_valid():
            prog_form = just_prog_form.save(commit=False)
            prog_form.author = request.user
            prog_form.save()
        return render(request, "Endeavors/endeavor_tasks.html", {"just_prog_form": just_prog_form,
                                                                 "multiple_form": multiple_form})

    else:
        just_prog_form = EndeavorModelForm()
    return render(request, "Endeavors/endeavor_tasks.html", {"just_prog_form": just_prog_form})


def tasks(request):
    number = 1
    program = Endeavor.objects.first()
    filled_multiple_tasks_form = MultipleTaskForms(request.GET)
    if filled_multiple_tasks_form.is_valid():
        number = filled_multiple_tasks_form.cleaned_data["number"]
    TaskFormSet = formset_factory(TaskModelForm1, extra=number)
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
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["goals"] = Endeavor.objects.filter(author=self.request.user)
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


# def endeavor_task_forms(request):
#     multiple_tasks = MultipleTaskForms()
#     if request.method == "POST":
#         endeavor_form = EndeavorModelForm(request.POST)
#         if endeavor_form.is_valid():
#             endeavor_form.save()
#             return redirect("list_endeavor")
#     else:
#         endeavor_form = EndeavorModelForm()
#     context = {
#         "endeavor_form": EndeavorModelForm,
#         "multiple_tasks": multiple_tasks
#     }
#     return render(request, "Endeavors/endeavor_task_forms.html", context)


# def tasks(request):
#     task_number = 2
#     multiple_task_forms = MultipleTaskForms(request.get)
#     if multiple_task_forms.is_valid():
#         task_number = multiple_task_forms.cleaned_data("number")
#     TaskFormSet= formset_factory(EndeavorModelForm, extra=task_number)
#     formset = TaskFormSet()
#     if request.method == "POST":
#         filled_formset = TaskFormSet(request)
#         if filled_formset.is_valid():
#             for form in filled_formset:
#                 print(form.cleaned_data["task_title"])
#             note = "Task have been registered"
#         else:
#             note = "Task was not created, try again"
#         return (request,"Endeavors/tasks.html", {"note": note, "formset": formset})
#     else:
#         return (request, "Endeavors/tasks.html", {"formset": formset})



