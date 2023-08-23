from django.test import SimpleTestCase
from django.urls import reverse


class UrlTests(SimpleTestCase):

    def test_url_exists_at_correct_location(self):

        """Log-in Route"""
        response_login = self.client.get("/")
        self.assertEqual(response_login.status_code, 200)

        """profile Route"""
        response_profile = self.client.get("/profile/")
        self.assertEqual(response_profile.status_code, 302)

        """Register Route"""
        response_register = self.client.get("/register/")
        self.assertEqual(response_register.status_code, 200)

        """Log-out Route"""
        response_logout = self.client.get("/logout/")
        self.assertEqual(response_logout.status_code, 200)

    def test_template_name_correct(self):

        """Log-in Route"""
        response_login = self.client.get("/")
        self.assertTemplateUsed(response_login, "users/login.html")

        """Register Route"""
        response_register = self.client.get("/register/")
        self.assertTemplateUsed(response_register, "users/register.html")

        """Log-out Route"""
        response_logout = self.client.get("/logout/")
        self.assertTemplateUsed(response_logout, "users/logout.html")
