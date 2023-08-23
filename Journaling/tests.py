from django.test import TestCase
from django.contrib.auth import get_user_model
from Journaling.models import Journal


class JournalModelLabelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com",
            password="testing321"
        )

        Journal.objects.create(author=cls.user, title="sleep early",
                               journal_date="2023-08-16", content="This is a new journal")

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
