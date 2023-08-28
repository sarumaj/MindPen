from django.test import TestCase, SimpleTestCase
from users.form import LoginForm


class UrlTests(SimpleTestCase):
    def test_login_url_exists_at_correct_location(self):
        response_login = self.client.get("/")
        self.assertEqual(response_login.status_code, 200)

    def test_profile_url_exists_at_correct_location(self):
        response_profile = self.client.get("/profile/")
        self.assertEqual(response_profile.status_code, 302)

    def test_register_url_exists_at_correct_location(self):
        response_register = self.client.get("/register/")
        self.assertEqual(response_register.status_code, 200)

    def test_logout_url_exists_at_correct_location(self):
        response_logout = self.client.get("/logout/")
        self.assertEqual(response_logout.status_code, 200)


class TemplateTests(SimpleTestCase):
    def test_Login_template_name_correct(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "users/login.html")

    def test_Register_template_name_correct(self):
        response = self.client.get("/register/")
        self.assertTemplateUsed(response, "users/register.html")

    def test_Logout_template_name_correct(self):
        response = self.client.get("/logout/")
        self.assertTemplateUsed(response, "users/logout.html")


class FormTests(TestCase):
    def test_login_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "secret12345",
            "password2": "secret12345"
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        form_data = {
            "username": "",
            "password1": "short",
            "password2": "no"
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
