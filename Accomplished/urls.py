from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.done, name="done"),
]