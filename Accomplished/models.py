from django.db import models


class Accomplishments(models.Model):
    summary = models.CharField(max_length=200)
    lessons_learned = models.TextField()

    def __str__(self):
        return self.summary
