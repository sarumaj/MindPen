from django import forms
from django.db import models
from django.contrib.auth.models import User
from MyMood.models import DataMood
from django.conf import settings


class Journal(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    journal_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-journal_date"]

    def __str__(self):
        return str(self.title)
