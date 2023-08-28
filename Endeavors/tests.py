from django.contrib.auth.models import User
from django.test import TestCase
from Endeavors.forms import EndeavorModelForm, MultipleTaskForms
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

    def test_list_endeavor_template_name_correct(self):
        response = self.client.get("/list_endeavor/")
        self.assertTemplateUsed(response, "Endeavors/list_endeavor.html")

    def test_detail_endeavor_template_name_correct(self):
        response = self.client.get(f"/detail_endeavor/{self.goal.id}/detail")
        # self.assertTemplateUsed(response, "Endeavors/detail_endeavor.html")
        self.assertEqual(response.headers["Location"], "/detail_endeavor/1/detail/")

    def test_delete_endeavor_template_name_correct(self):
        response = self.client.get(f"/delete_endeavor/{self.goal.id}/delete")
        # self.assertTemplateUsed(response, "Endeavors/delete_endeavor.html")
        self.assertEqual(response.headers["Location"], "/delete_endeavor/1/delete/")

    def test_tasks_related_to_endeavor_template_name_correct(self):
        response = self.client.get("/tasks/")
        self.assertTemplateUsed(response, "Endeavors/tasks.html")

    def test_create_endeavor_template_name_correct(self):
        response = self.client.get("/create_endeavor/")
        self.assertTemplateUsed(response, "Endeavors/endeavor_tasks.html")


class EndeavorModelLabelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        Endeavor.objects.create(
            author=self.user,
            title="sleep early",
            start_date="2023-08-16"
        )

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

    def test_count_endeavor_objects(self):
        response = Endeavor.objects.all().count()
        self.assertEquals(response, 1)


class FormTests(TestCase):
    def test_endeavor_model_form_valid_data(self):
        form_data = {
            "title": "Test Endeavor",
            "start_date": "2023-08-28"
        }
        form = EndeavorModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_endeavor_model_form_invalid_data(self):
        form_data = {
            "title": "",
            "start_date": "invalid_date"
        }
        form = EndeavorModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_multiple_task_forms_valid_number_of_tasks(self):
        form_data = {
            "number_of_tasks": 3
        }
        form = MultipleTaskForms(data=form_data)
        self.assertTrue(form.is_valid())

    def test_multiple_task_forms_invalid_number_of_tasks_below_min(self):
        form_data = {
            "number_of_tasks": 0
        }
        form = MultipleTaskForms(data=form_data)
        self.assertFalse(form.is_valid())

    def test_multiple_task_forms_invalid_number_of_tasks_above_max(self):
        form_data = {
            "number_of_tasks": 6
        }
        form = MultipleTaskForms(data=form_data)
        self.assertFalse(form.is_valid())
