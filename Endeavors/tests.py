from django.test import TestCase
from django.contrib.auth import get_user_model
from Endeavors.models import Endeavor


class EndeavorModelLabelsTest(TestCase):
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
