from django.db import models


class DataMood(models.Model):
    mood = models.CharField(max_length=30)
    mood_score = models.IntegerField()
    mood_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mood
