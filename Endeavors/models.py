from django.db import models


class Endeavor(models.Model):
    program_title = models.CharField(max_length=100, null=True, unique=True)
    start_day = models.DateField(null=True)
    duration = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.program_title
