from django.db import models
from Endeavors.models import Endeavor


class Task(models.Model):
    endeavor = models.ForeignKey(Endeavor, on_delete=models.CASCADE, null=True, related_name="todo_tasks")
    task_title = models.CharField(max_length=200, null=True, unique=True)
    set_time = models.TimeField(null=True)
    is_done = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.task_title
