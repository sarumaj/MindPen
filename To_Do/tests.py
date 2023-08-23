from django.test import TestCase
from django.contrib.auth import get_user_model
from To_Do.models import Task
from Endeavors.models import Endeavor


class TaskModelLabelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com",
            password="testing321"
        )
        cls.goal = Endeavor.objects.create(author=cls.user, title="sleep early",
                                           start_date="2023-08-24")

        Task.objects.create(goal=cls.goal, title="task 1", description= "Empty",
                            starting_time="2023-08-24 15:32:00", completed=False)

    def test_goal_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field("goal").verbose_name
        self.assertEqual(field_label, "goal")

    def test_starting_time_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field("starting_time").verbose_name
        self.assertEqual(field_label, "starting time")

    def test_title_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)

    def test_string_representation_of_objects(self):
        task = Task.objects.get(id=1)
        self.assertEqual(str(task), task.title)

