from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import User
from To_Do.models import Task
from Endeavors.models import Endeavor
from django.urls import reverse


class UrlTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.client.login(username="testuser", password="secret")

    def test_todos_url_exists_at_correct_location(self):
        goal = Endeavor.objects.create(
            author=self.user,
            start_date="2023-08-11",
            title="slim try",
        )
        Task.objects.create(
            goal=goal,
            starting_time="2023-08-17 15:32:00",
            title="task1",
        )
        response = self.client.get("/todos/")
        self.assertEqual(response.status_code, 200)

    def test_detail_todo_url_exists_at_correct_location(self):
        goal = Endeavor.objects.create(
            author=self.user,
            start_date="2023-08-11",
            title="slim try",
        )
        task1 = Task.objects.create(
            goal=goal,
            starting_time="2023-08-17 15:32:00",
            title="task1",
        )
        response = self.client.get(f"/detail_todo/{task1.id}/detail/")
        self.assertEqual(response.status_code, 200)

    def test_delete_todo_url_exists_at_correct_location(self):
        goal = Endeavor.objects.create(
            author=self.user,
            start_date="2023-08-11",
            title="slim try",
        )
        task1 = Task.objects.create(
            goal=goal,
            starting_time="2023-08-17 15:32:00",
            title="task1",
        )
        response = self.client.get(f"/delete_todo/{task1.id}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_update_todo_url_exists_at_correct_location(self):
        goal = Endeavor.objects.create(
            author=self.user,
            start_date="2023-08-11",
            title="slim try",
        )
        task1 = Task.objects.create(
            goal=goal,
            starting_time="2023-08-17 15:32:00",
            title="task1",
        )
        response = self.client.get(f"/update_todo/{task1.id}/update/")
        self.assertEqual(response.status_code, 200)

    def test_create_todo_url_exists_at_correct_location(self):
        goal = Endeavor.objects.create(
            author=self.user,
            start_date="2023-08-11",
            title="slim try",
        )
        task1 = Task.objects.create(
            goal=goal,
            starting_time="2023-08-17 15:32:00",
            title="task1",
        )

        response = self.client.get(reverse("create_todo", kwargs={"program": goal}))
        self.assertEqual(response.status_code, 200)


class TaskModelLabelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com",
            password="testing321"
        )
        cls.goal = Endeavor.objects.create(author=cls.user, title="sleep early",
                                           start_date="2023-08-24")

        Task.objects.create(goal=cls.goal, title="task 1", description="Empty",
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
