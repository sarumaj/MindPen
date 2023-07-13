from django.db import models


class Person(models.Model):
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Post(models.Model):
    content = models.TextField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.content
