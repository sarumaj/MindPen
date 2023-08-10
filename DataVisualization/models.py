from django.db import models
from django.contrib.auth.models import User


class PreviousMonth (models.Model):
    average = models.FloatField()
    date = models.CharField(max_length=10)

    def __str__(self):
        return self.date
