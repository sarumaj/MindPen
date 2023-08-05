from django import forms
from django.db import models
from django.contrib.auth.models import User
from MyMood.models import DataMood


class Journal(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    journal_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    mood = models.OneToOneField(DataMood, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["-journal_date"]

    def __str__(self):
        return str(self.title)

    # def get_absolute_url(self):
    #     return reverse('journal_detail', kwargs={'pk': self.pk})

