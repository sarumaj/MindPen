from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Journal
from django.contrib.auth.models import User


class UrlTests(TestCase):
    def test_journal_url_exists_at_correct_location(self):
        response = self.client.get("/journal/")
        self.assertEqual(response.status_code, 302)

    def test_journal_detail_url_exists_at_correct_location(self):
        slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        first = Journal.objects.create(
            author=slim,
            journal_date="2023-08-11 04:49:05.716458",
            title="slim try",
            content="test",
        )
        response = self.client.get(f"/journal/{first.id}")
        self.assertEqual(response.status_code, 301)

    def test_journal_update_url_exists_at_correct_location(self):
        slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        first = Journal.objects.create(
            author=slim,
            journal_date="2023-08-11 04:49:05.716458",
            title="slim try",
            content="test",
        )
        response = self.client.get(f"/journal/{first.id}/update/")
        self.assertEqual(response.status_code, 302)

    def test_journal_delete_url_exists_at_correct_location(self):
        slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        first = Journal.objects.create(
            author=slim,
            journal_date="2023-08-11 04:49:05.716458",
            title="slim try",
            content="test",
        )
        response = self.client.get(f"/journal/{first.id}/delete/")
        self.assertEqual(response.status_code, 302)


class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.client.login(username="slim", password="secret")

    def test_journal_template_name_correct(self):
        response = self.client.get(reverse("journal"))
        self.assertEqual(response.headers["Location"], "/?next=/journal/")

    def test_journal_detail_msg_template_name_correct(self):
        first = Journal.objects.create(
                author=self.user,
                journal_date="2023-08-11 04:49:05.716458",
                title="slim try",
                content="test",
            )
        response = self.client.get(f"/journal/{first.id}/")
        self.assertEqual(response.headers["Location"], "/?next=/journal/1/")

    def test_journal_update_msg_template_name_correct(self):
        first = Journal.objects.create(
                author=self.user,
                journal_date="2023-08-11 04:49:05.716458",
                title="slim try",
                content="test",
            )
        response = self.client.get(f"/journal/{first.id}/update/")
        self.assertEqual(response.headers["Location"], "/?next=/journal/1/update/")

    def test_journal_delete_msg_template_name_correct(self):
        first = Journal.objects.create(
                author=self.user,
                journal_date="2023-08-11 04:49:05.716458",
                title="slim try",
                content="test",
            )
        response = self.client.get(f"/journal/{first.id}/delete/")
        self.assertEqual(response.headers["Location"], "/?next=/journal/1/delete/")


class JournalModelLabelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com",
            password="testing321"
        )

        Journal.objects.create(author=cls.user,
                               title="sleep early",
                               journal_date="2023-08-16",
                               content="This is a new journal"
                               )

    def test_author_label(self):
        journal = Journal.objects.get(id=1)
        field_label = journal._meta.get_field("author").verbose_name
        self.assertEqual(field_label, "author")

    def test_journal_date_label(self):
        journal = Journal.objects.get(id=1)
        field_label = journal._meta.get_field("journal_date").verbose_name
        self.assertEqual(field_label, "journal date")

    def test_title_length(self):
        journal = Journal.objects.get(id=1)
        max_length = journal._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_string_representation_of_objects(self):
        journal = Journal.objects.get(id=1)
        self.assertEqual(str(journal), journal.title)

    def test_count_journal_objects(self):
        response = Journal.objects.all().count()
        self.assertEquals(response, 1)
