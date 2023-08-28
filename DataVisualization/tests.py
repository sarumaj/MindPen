from django.test import TestCase
from django.contrib.auth import get_user_model
from DataVisualization.models import PreviousMonth


class UrlTests(TestCase):
    def test_data_url_exists_at_correct_location(self):
        response = self.client.get("/data/")
        self.assertEqual(response.status_code, 302)


class TemplateTests(TestCase):
    def test_data_template_name_correct(self):
        response = self.client.get("/data/")
        self.assertEqual(response.headers["Location"], "/?next=/data/")


class PreviousMonthModelLabelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testing321"
        )
        PreviousMonth.objects.create(user=self.user, average=4.2, date="2023-07")

    def test_user_label(self):
        previous_month = PreviousMonth.objects.get(id=1)
        field_label = previous_month._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_average_label(self):
        previous_month = PreviousMonth.objects.get(id=1)
        field_label = previous_month._meta.get_field("average").verbose_name
        self.assertEqual(field_label, "average")

    def test_date_length(self):
        previous_month = PreviousMonth.objects.get(id=1)
        max_length = previous_month._meta.get_field("date").max_length
        self.assertEqual(max_length, 10)
