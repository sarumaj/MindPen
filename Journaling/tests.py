from django.test import TestCase
from django.urls import reverse
from .forms import JournalModelForm
from .models import Journal
from django.contrib.auth.models import User


class UrlTests(TestCase):
    def setUp(self):
        self.slim = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.first = Journal.objects.create(
            author=self.slim,
            journal_date="2023-08-11 04:49:05.716458",
            title="slim try",
            content="test",
        )

    def test_journal_url_exists_at_correct_location(self):
        response = self.client.get("/journal/")
        self.assertEqual(response.status_code, 302)

    def test_journal_detail_url_exists_at_correct_location(self):
        response = self.client.get(f"/journal/{self.first.id}")
        self.assertEqual(response.status_code, 301)

    def test_journal_update_url_exists_at_correct_location(self):
        response = self.client.get(f"/journal/{self.first.id}/update/")
        self.assertEqual(response.status_code, 302)

    def test_journal_delete_url_exists_at_correct_location(self):
        response = self.client.get(f"/journal/{self.first.id}/delete/")
        self.assertEqual(response.status_code, 302)


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
            journal_date="2023-08-11 04:49:05.716458",
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


class FormTests(TestCase):
    def test_journal_model_form_valid_data(self):
        form_data = {
            "title": "Test Journal",
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
