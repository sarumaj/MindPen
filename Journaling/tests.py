from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import JournalModelForm
from .models import Journal
import datetime

User = get_user_model()


class UrlTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.client.login(username="testuser", password="secret")

        self.first = Journal.objects.create(
            author=self.user,
            journal_date=datetime.datetime(2025, 2, 1, 4, 49, 5),  # Correct format
            title="slim try",
            content="test",
        )

    def test_journal_url_exists_at_correct_location(self):
        response = self.client.get("/journal/")
        self.assertEqual(response.status_code, 200)

    def test_journal_detail_url_exists_at_correct_location(self):
        response = self.client.get(f"/journal/{self.first.id}/")
        self.assertEqual(response.status_code, 200)

    def test_journal_update_url_exists_at_correct_location(self):
        response = self.client.get(f"/journal/{self.first.id}/update/")
        self.assertEqual(response.status_code, 200)

    def test_journal_delete_url_exists_at_correct_location(self):
        response = self.client.get(f"/journal/{self.first.id}/delete/")
        self.assertEqual(response.status_code, 200)


class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.client.login(username="testuser", password="secret")

        self.first = Journal.objects.create(
            author=self.user,
            journal_date=datetime.datetime(2025, 2, 1, 4, 49, 5),
            title="slim try",
            content="test",
        )

    def test_journal_template_name_correct(self):
        response = self.client.get(reverse("journal"))
        self.assertTemplateUsed(response, "Journaling/journal.html")

    def test_journal_detail_msg_template_name_correct(self):
        response = self.client.get(f"/journal/{self.first.id}/")
        self.assertTemplateUsed(response, "Journaling/detail_journal.html")

    def test_journal_update_msg_template_name_correct(self):
        response = self.client.get(f"/journal/{self.first.id}/update/")
        self.assertTemplateUsed(response, "Journaling/update.html")

    def test_journal_delete_msg_template_name_correct(self):
        response = self.client.get(f"/journal/{self.first.id}/delete/")
        self.assertTemplateUsed(response, "Journaling/delete.html")


class JournalModelLabelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )

        Journal.objects.create(
            author=self.user,
            title="sleep early",
            journal_date=datetime.datetime(2025, 2, 1, 12, 0, 0),  # Corrected
            content="This is a new journal"
        )

    def test_author_label(self):
        journal = Journal.objects.first()
        field_label = journal._meta.get_field("author").verbose_name
        self.assertEqual(field_label, "author")

    def test_journal_date_label(self):
        journal = Journal.objects.first()
        field_label = journal._meta.get_field("journal_date").verbose_name
        self.assertEqual(field_label, "journal date")

    def test_title_length(self):
        journal = Journal.objects.first()
        max_length = journal._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_string_representation_of_objects(self):
        journal = Journal.objects.first()
        self.assertEqual(str(journal), journal.title)

    def test_count_journal_objects(self):
        response = Journal.objects.all().count()
        self.assertEqual(response, 1)


class FormTests(TestCase):
    def test_journal_model_form_valid_data(self):
        form_data = {
            "title": "I could sort the To_Do's",
            "content": "Test"
        }
        form = JournalModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_journal_model_form_invalid_data(self):
        form_data = {
            "title": "",
            "content": ""
        }
        form = JournalModelForm(data=form_data)
        self.assertFalse(form.is_valid())
