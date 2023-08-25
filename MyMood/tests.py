from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model
from MyMood.models import DataMood


class UrlTests(TestCase):
    def test_mood_url_exists_at_correct_location(self):
        response = self.client.get("/mood/")
        self.assertEqual(response.status_code, 302)

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
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com",
            password="testing321"
        )

        DataMood.objects.create(user=cls.user, mood_score=2, mood_date="2023-08-16")

    def test_user_label(self):
        data_mood = DataMood.objects.get(id=1)
        field_label = data_mood._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_mood_date_label(self):
        data_mood = DataMood.objects.get(id=1)
        field_label = data_mood._meta.get_field("mood_date").verbose_name
        self.assertEqual(field_label, "mood date")

    def test_mood_score_length(self):
        data_mood = DataMood.objects.get(id=1)
        max_length = data_mood._meta.get_field("mood_score").max_length
        self.assertEqual(max_length, 2)

    def test_string_representation_of_objects(self):
        data_mood = DataMood.objects.get(id=1)
        self.assertEqual(str(data_mood), data_mood.mood_score)
