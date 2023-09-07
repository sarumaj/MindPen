from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from Endeavors.models import Endeavor
from .models import Task
from .forms import TaskModelForm2
from django.core.paginator import Paginator


class TaskListView(ListView):
    model = Task
    template_name = "To_Do/to_do.html"
    ordering = ["id"]
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(endeavor__author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve all goals and tasks for the current user
        goal_list = Endeavor.objects.filter(author=self.request.user)
        task_list = Task.objects.filter(endeavor__author=self.request.user)
        goal_task_list = []
        # Iterate through goals and associate tasks with their respective goals
        for goal in goal_list:
            tasks_for_goal = [task for task in task_list if task.endeavor == goal]
            goal_task_list.append({"goal": goal, "tasks": tasks_for_goal})

        # Create a Paginator instance for the list of goal-task dictionaries
        paginator = Paginator(goal_task_list, 3)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["programs"] = page_obj
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
        # Retrieve the program title from URL parameters
        program_title = self.kwargs.get("program")
        program = Endeavor.objects.get(title=program_title)
        initial["endeavor"] = program
        return initial


class TasklUpdateView(UpdateView):
    model = Task
    template_name = "To_Do/update_task.html"
    fields = ["title", "starting_time", "completed"]
    success_url = "/todos/"
