from django.db import models


class Journal(models.Model):
    journal_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    class Meta:
        ordering = ["-journal_date"]

    def __str__(self):
        return str(self.title)

