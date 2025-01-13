from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class LoginForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "phone_number", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["username", "phone_number", "password1", "password2"]:
            self.fields[field].help_text = None



class LoginForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Remove help_text for the specified fields.
        for field in ["username", "password1", "password2"]:
            self.fields[field].help_text = None

    class Meta:
        model = CustomUser
        fields = ["username", "phone_number","password1", "password2"]