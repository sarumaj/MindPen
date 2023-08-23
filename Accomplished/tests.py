from django.test import TestCase
from django.contrib.auth import get_user_model
from Accomplished.models import AccomplishedGoal


class AccomplishedGoalModelLabelsTest(TestCase):
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
