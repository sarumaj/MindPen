from django.views.generic import ListView, DetailView, DeleteView, CreateView
from Endeavors.models import Task, Endeavor
from Endeavors.forms import TaskModelForm


class TaskListView(ListView):
    model = Task
    template_name = "To_Do/to_do.html"
    context_object_name = "tasks"
    extra_context = {'programs': Endeavor.objects.all()}


class TaskDetailView(DetailView):
    model = Task
    template_name = "To_Do/detail_todo.html"


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "To_Do/delete_todo.html"
    success_url = "/todos/"


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskModelForm
    template_name = "To_Do/create_task.html"
    success_url = "/todos/"