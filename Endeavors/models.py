from django.db import models


class Endeavor(models.Model):
    program_title = models.CharField(max_length=100, null=True, unique=True)
    start_day = models.DateField(null=True)
    duration = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.program_title


class Task(models.Model):

    task_title = models.CharField(max_length=200, null=True, unique=True)
    set_time = models.TimeField(null=True)
    is_done = models.BooleanField(default=False, null=True, blank=True)
    endeavor = models.ForeignKey(Endeavor, on_delete=models.CASCADE, null=True, related_name="tasks")

    def __str__(self):
        return self.task_title
