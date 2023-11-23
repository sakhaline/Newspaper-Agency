from django.contrib.auth import get_user_model
from django.test import TestCase

from media.models import Topic, Newspaper


class ModelTests(TestCase):
    def test_newspaper_str(self):
        topic = Topic.objects.create(name="Technologies")
        newspaper = Newspaper.objects.create(
            title="Tech Wonders: Innovations in 2023",
            content=("Discover the cutting-edge technologies"
                     "and trends revolutionizing our digital future."),
            topic=topic,
        )
        self.assertEqual(str(newspaper), newspaper.title)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create_user(
            username="alice52",
            password="dddeeeeFFFFF54321",
        )
        self.assertEqual(str(redactor), "alice52")

    def test_topic_str(self):
        topic = Topic.objects.create(name="Technologies")
        self.assertEqual(str(topic), topic.name)

    def test_create_redactor_with_years_of_experience(self):
        years_of_experience = 17
        redactor = get_user_model().objects.create_user(
            username="alice52",
            password="dddeeeeFFFFF54321",
            years_of_experience=years_of_experience
        )
        self.assertEqual(redactor.years_of_experience, years_of_experience)
