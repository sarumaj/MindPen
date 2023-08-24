from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model
from Endeavors.models import Endeavor


class UrlTests(TestCase):
    def test_list_endeavor_url_exists_at_correct_location(self):
        response = self.client.get("/list_endeavor/")
        self.assertEqual(response.status_code, 302)

    def test_create_endeavor_url_exists_at_correct_location(self):
        response = self.client.get("/create_endeavor/")
        self.assertEqual(response.status_code, 200)

    def test_create_task_for_endeavor_url_exists_at_correct_location(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)

    def test_detail_endeavor_url_exists_at_correct_location(self):
        slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        goal = Endeavor.objects.create(
            author=slim,
            start_date="2023-08-11",
            title="slim try",
        )
        response = self.client.get(f"/detail_endeavor/{goal.id}/detail/")
        self.assertEqual(response.status_code, 302)

    def test_delete_endeavor_url_exists_at_correct_location(self):
        slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        goal = Endeavor.objects.create(
            author=slim,
            start_date="2023-08-11",
            title="slim try",
        )
        response = self.client.get(f"/detail_endeavor/{goal.id}/detail/")
        self.assertEqual(response.status_code, 302)


class EndeavorModelLabelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com",
            password="testing321"
        )

        Endeavor.objects.create(author=cls.user, title="sleep early", start_date="2023-08-16")

    def test_author_label(self):
        endeavor = Endeavor.objects.get(id=1)
        field_label = endeavor._meta.get_field("author").verbose_name
        self.assertEqual(field_label, "author")

    def test_start_date_label(self):
        endeavor = Endeavor.objects.get(id=1)
        field_label = endeavor._meta.get_field("start_date").verbose_name
        self.assertEqual(field_label, "start date")

    def test_title_length(self):
        endeavor = Endeavor.objects.get(id=1)
        max_length = endeavor._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_string_representation_of_objects(self):
        endeavor = Endeavor.objects.get(id=1)
        self.assertEqual(str(endeavor), endeavor.title)

    def test_count_journal_objects(self):
        response = Endeavor.objects.all().count()
        self.assertEquals(response, 1)
