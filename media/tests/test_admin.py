from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from media.models import Topic, Newspaper


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="aaabbbbCCCCC54321"
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="alice52",
            password="dddeeeeFFFFF54321",
            years_of_experience=12
        )
        self.topic = Topic.objects.create(name="Technologies")
        self.newspaper = Newspaper.objects.create(
            title="Tech Wonders: Innovations in 2023", topic=self.topic
        )

    def test_topic_admin_page(self):
        url = reverse("admin:newspaper_topic_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_newspaper_admin_page(self):
        response = self.client.get(reverse("admin:newspaper_newspaper_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_redactor_admin_page(self):
        response = self.client.get(reverse("admin:newspaper_redactor_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_newspaper_admin_filter(self):
        url = reverse("admin:newspaper_newspaper_changelist")
        response = self.client.get(url, {"topic__id__exact": self.topic.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech Wonders: Innovations in 2023")

    def test_newspaper_admin_search(self):
        url = reverse("admin:newspaper_newspaper_changelist")
        response = self.client.get(url, {"q": "Tech Wonders: Innovations in 2023"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech Wonders: Innovations in 2023")
