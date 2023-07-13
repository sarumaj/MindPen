from django.db import models


class ToDo(models.Model):
    tile = models.CharField(max_length=200)
    task_status = models.BooleanField()

    def __str__(self):
        return self.tile
