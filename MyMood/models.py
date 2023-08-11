from django.db import models
from django.contrib.auth.models import User


class DataMood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mood_score = models.CharField(max_length=2)
    mood_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.mood_score

