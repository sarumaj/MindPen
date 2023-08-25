from django.test import SimpleTestCase


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
