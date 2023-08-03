from django.contrib.auth.models import User
from django.db import models


class AccomplishedGoal (models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    program_title = models.CharField(max_length=100, null=True, unique=True)
    start_day = models.DateField(null=True)
    end_day = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.program_title