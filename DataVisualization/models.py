from django.db import models
from django.contrib.auth.models import User


class PreviousMonth (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    average = models.FloatField()
    date = models.CharField(max_length=10)

    def __str__(self):
        return self.date

    # class Meta:
    #     ordering = ["-id"]
