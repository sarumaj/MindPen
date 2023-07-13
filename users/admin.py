from django.contrib import admin
from .models import Person, Post

admin.site.register(Person)
admin.site.register(Post)