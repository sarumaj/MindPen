from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from Endeavors.models import Endeavor
from .models import Task
from .forms import TaskModelForm2


class TaskListView(ListView):
    model = Task
    template_name = "To_Do/to_do.html"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["programs"] = Endeavor.objects.filter(author=self.request.user)
        context["tasks"] = Task.objects.filter(goal__author=self.request.user)
        return context


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
        program = Endeavor.objects.get(title=program_title)
        initial["goal"] = program
        return initial


class TasklUpdateView(UpdateView):
    model = Task
    template_name = "To_Do/update_task.html"
    fields = ["title", "starting_time", "completed"]
    success_url = "/todos/"