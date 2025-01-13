from django.db import models
from django.contrib.auth.models import User


class DataMood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mood_score = models.IntegerField()
    mood_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.mood_score)


class PreviousMonth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    average = models.FloatField()
    date = models.CharField(max_length=10)

    def __str__(self):
        return self.date
