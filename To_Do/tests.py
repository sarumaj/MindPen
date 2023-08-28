from django.test import TestCase
from django.contrib.auth.models import User
from To_Do.forms import TaskModelForm1, TaskModelForm2
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

        self.goal = Endeavor.objects.create(
            author=self.user,
            start_date="2023-08-11",
            title="slim try"
        )

    def test_todos_url_exists_at_correct_location(self):
        Task.objects.create(
            goal=self.goal,
            starting_time="2023-08-17 15:32:00",
            title="task1"
        )
        response = self.client.get("/todos/")
        self.assertEqual(response.status_code, 200)

    def test_detail_todo_url_exists_at_correct_location(self):
        task1 = Task.objects.create(
            goal=self.goal,
            starting_time="2023-08-17 15:32:00",
            title="task1"
        )
        response = self.client.get(f"/detail_todo/{task1.id}/detail/")
        self.assertEqual(response.status_code, 200)

    def test_delete_todo_url_exists_at_correct_location(self):
        task1 = Task.objects.create(
            goal=self.goal,
            starting_time="2023-08-17 15:32:00",
            title="task1"
        )
        response = self.client.get(f"/delete_todo/{task1.id}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_update_todo_url_exists_at_correct_location(self):
        task1 = Task.objects.create(
            goal=self.goal,
            starting_time="2023-08-17 15:32:00",
            title="task1"
        )
        response = self.client.get(f"/update_todo/{task1.id}/update/")
        self.assertEqual(response.status_code, 200)

    def test_create_todo_url_exists_at_correct_location(self):
        Task.objects.create(
            goal=self.goal,
            starting_time="2023-08-17 15:32:00",
            title="task1"
        )

        response = self.client.get(reverse("create_todo", kwargs={"program": self.goal}))
        self.assertEqual(response.status_code, 200)


class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.client.login(username="testuser", password="secret")

        self.goal = Endeavor.objects.create(
            author=self.user,
            start_date="2023-08-11",
            title="slim try",
        )
        self.task = Task.objects.create(
            goal=self.goal,
            starting_time="2023-08-17 15:32:00",
            title="task1",
        )

    def test_todos_template_name_correct(self):
        response = self.client.get("/todos/")
        self.assertTemplateUsed(response, "To_Do/to_do.html")

    def test_detail_todo_template_name_correct(self):
        response = self.client.get(f"/detail_todo/{self.task.id}/detail/")
        self.assertTemplateUsed(response, "To_Do/detail_todo.html")

    def test_delete_todo_template_name_correct(self):
        response = self.client.get(f"/delete_todo/{self.task.id}/delete/")
        self.assertTemplateUsed(response, "To_Do/delete_todo.html")

    def test_create_todo_template_name_correct(self):
        response = self.client.get(reverse("create_todo", kwargs={"program": self.goal}))
        self.assertTemplateUsed(response, "To_Do/create_task.html")

    def test_update_todo_template_name_correct(self):
        response = self.client.get(f"/update_todo/{self.task.id}/update/")
        self.assertTemplateUsed(response, "To_Do/update_task.html")


class TaskModelLabelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.goal = Endeavor.objects.create(
            author=self.user,
            title="sleep early",
            start_date="2023-08-24"
        )

        Task.objects.create(
            goal=self.goal,
            title="task 1",
            description="Empty",
            starting_time="2023-08-24 15:32:00",
            completed=False
        )

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


class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.client.login(username="testuser", password="secret")

        self.endeavor = Endeavor.objects.create(
            title="Goal Test",
            start_date="2023-08-17",
            author=self.user
        )

    def test_task_model_form1_valid_data(self):
        form_data = {
            "title": "Test Task",
            "starting_time": "2023-08-17 15:32:00",
            "completed": False,
        }
        form = TaskModelForm1(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_model_form1_invalid_data(self):
        form_data = {
            "title": "",
            "starting_time": "invalid_datetime",
            "completed": "invalid_completed",
        }
        form = TaskModelForm1(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_model_form2_valid_data(self):
        form_data = {
            "goal": self.endeavor.id,
            "title": "Test Task",
            "starting_time": "2023-08-17 15:32:00",
            "completed": False,
        }
        form = TaskModelForm2(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_model_form2_invalid_data(self):
        form_data = {
            "goal": self.endeavor.id,
            "title": "",
            "starting_time": "invalid_datetime",
            "completed": "invalid_completed",
        }
        form = TaskModelForm2(data=form_data)
        self.assertFalse(form.is_valid())
