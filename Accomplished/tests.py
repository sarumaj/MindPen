from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from Accomplished.models import AccomplishedGoal


class UrlTests(TestCase):
    def test_done_url_exists_at_correct_location(self):
        slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        AccomplishedGoal.objects.create(
            author=slim,
            program_title="run",
            start_day="2023-08-24",
            end_day="2023-08-25"
        )
        response = self.client.get("/done/")
        self.assertEqual(response.status_code, 302)

    def test_done_update_url_exists_at_correct_location(self):
        slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        done1 = AccomplishedGoal.objects.create(
            author=slim,
            program_title="run",
            start_day="2023-08-24",
            end_day="2023-08-25"
        )
        response = self.client.get(f"/done_update/{done1.id}/")
        self.assertEqual(response.status_code, 302)

    def test_done_delete_url_exists_at_correct_location(self):
        slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        done1 = AccomplishedGoal.objects.create(
            author=slim,
            program_title="run",
            start_day="2023-08-24",
            end_day="2023-08-25"
        )
        response_register = self.client.get(f"/done_delete/{done1.id}/")
        self.assertEqual(response_register.status_code, 302)


class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.client.login(username="slim", password="secret")

    def test_journal_template_name_correct(self):
        response = self.client.get("/done/")
        self.assertEqual(response.headers["Location"], "/?next=/done/")

    def test_done_update_template_name_correct(self):
        done1 = AccomplishedGoal.objects.create(
            author=self.user,
            program_title="run",
            start_day="2023-08-24",
            end_day="2023-08-25"
        )
        response = self.client.get(f"/done_update/{done1.id}/")
        self.assertEqual(response.headers["Location"], "/?next=/done_update/1/")

    def test_done_delete_template_name_correct(self):
        done1 = AccomplishedGoal.objects.create(
            author=self.user,
            program_title="run",
            start_day="2023-08-24",
            end_day="2023-08-25"
        )
        response = self.client.get(f"/done_delete/{done1.id}/")
        self.assertEqual(response.headers["Location"], "/?next=/done_delete/1/")


class AccomplishedGoalModelLabelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com",
            password="testing321"
        )

        AccomplishedGoal.objects.create(author=cls.user, program_title="sleep early",
                                        start_day="2023-08-16", end_day="2023-08-16",
                                        summary="That's was a great lesson")

    def test_author_label(self):
        completed = AccomplishedGoal.objects.get(id=1)
        field_label = completed._meta.get_field("author").verbose_name
        self.assertEqual(field_label, "author")

    def test_start_day_label(self):
        completed = AccomplishedGoal.objects.get(id=1)
        field_label = completed._meta.get_field("start_day").verbose_name
        self.assertEqual(field_label, "start day")

    def test_program_title_length(self):
        completed = AccomplishedGoal.objects.get(id=1)
        max_length = completed._meta.get_field("program_title").max_length
        self.assertEqual(max_length, 100)

    def test_string_representation_of_objects(self):
        completed = AccomplishedGoal.objects.get(id=1)
        self.assertEqual(str(completed), completed.program_title)
