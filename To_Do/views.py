from django.views.generic import ListView, DetailView, DeleteView, CreateView
from Endeavors.models import Endeavor
from .models import Task
from .forms import TaskModelForm2


class TaskListView(ListView):
    model = Task
    template_name = "To_Do/to_do.html"
    context_object_name = "tasks"
    extra_context = {'programs': Endeavor.objects.all()}


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