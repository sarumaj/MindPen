from django.urls import path
from .views import verify_phone

urlpatterns = [
    path("verify/", verify_phone, name="verify_phone")
]
