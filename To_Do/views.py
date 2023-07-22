from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from Endeavors.models import Endeavor
from .models import Task
from .forms import TaskModelForm2


class TaskListView(ListView):
    model = Task
    template_name = "To_Do/to_do.html"
    context_object_name = "tasks"
    extra_context = {'programs': Endeavor.objects.all()}
    ordering = ["-id"]


class TaskDetailView(DetailView):
    model = Task
    template_name = "To_Do/detail_todo.html"
    context_object_name = "post"


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "To_Do/delete_todo.html"
    success_url = "/todos/"


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskModelForm2
    template_name = "To_Do/create_task.html"
    success_url = "/todos/"

    def get_initial(self):
        initial = super().get_initial()
        program_title = self.kwargs.get("program")  # Retrieve the program title from URL parameters
        program = Endeavor.objects.get(program_title=program_title)
        initial["endeavor"] = program
        return initial


class TasklUpdateView(UpdateView):
    model = Task
    template_name = "To_Do/update_task.html"
    fields = ["task_title", "set_time"]
    success_url = "/todos/"