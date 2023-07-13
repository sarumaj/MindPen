from . import views
from django.urls import path
from .views import ProfileTemplateViews

urlpatterns = [
        path('', views.register, name="register"),
        path('profile/', ProfileTemplateViews.as_view(), name="profile"),
]
