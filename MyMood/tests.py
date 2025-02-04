from django.contrib.auth import get_user_model
from django.test import TestCase
from MyMood.forms import MoodModelForm
from MyMood.models import DataMood
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

    def test_mood_url_exists_at_correct_location(self):
        response = self.client.get("/mood/")
        self.assertEqual(response.status_code, 200)

    def test_mood_msg_url_exists_at_correct_location(self):
        response = self.client.get("/mood_msg/")
        self.assertEqual(response.status_code, 200)

class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        self.client.login(username="testuser", password="secret")

    def test_mood_template_name_correct(self):
        response = self.client.get("/mood/")
        self.assertTemplateUsed(response, "MyMood/mood.html")

    def test_mood_msg_template_name_correct(self):
        response = self.client.get("/mood_msg/")
        self.assertTemplateUsed(response, "MyMood/mood_message.html")

class MyMoodModelLabelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        DataMood.objects.create(
            user=self.user,
            mood_score=1,
            mood_date=datetime.date(2025, 2, 1)
        )

    def test_user_label(self):
        data_mood = DataMood.objects.first()
        field_label = data_mood._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_mood_date_label(self):
        data_mood = DataMood.objects.first()
        field_label = data_mood._meta.get_field("mood_date").verbose_name
        self.assertEqual(field_label, "mood date")

    def test_string_representation_of_objects(self):
        data_mood = DataMood.objects.first()
        self.assertEqual(1, data_mood.mood_score)

class FormTests(TestCase):
    def test_mood_model_form_valid_data(self):
        form_data = {
            "mood_score": 1
        }
        form = MoodModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_mood_model_form_invalid_data(self):
        form_data = {
            "mood_score": "invalid"
        }
        form = MoodModelForm(data=form_data)
        self.assertFalse(form.is_valid())
