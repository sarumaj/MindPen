from django.contrib.auth.models import User
from django.db import models


class Endeavor(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, unique=True)
    start_date = models.DateField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]
