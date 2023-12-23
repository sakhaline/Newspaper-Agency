from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from agency.models import Newspaper, Topic


class AdminSiteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="testAdminUsername",
            password="testAdminPassword",
        )
        self.client.force_login(self.admin_user)

        self.redactor = get_user_model().objects.create_user(
            username="testUsername",
            password="testUserPassword",
            years_of_experience=5,
        )

        self.topic = Topic.objects.create(
            name="testTopic",
        )

        self.newspaper = Newspaper.objects.create(
            title="testNewspaper title",
            content="testNewspaper content",
            topic=self.topic,
        )

    def test_redactor_list_years_of_experience_listed(self):
        url = reverse("admin:agency_redactor_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_detail_years_of_experience_listed(self):
        url = reverse("admin:agency_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)

        self.assertContains(response, self.redactor.years_of_experience)

    def test_newspaper_list(self):
        url = reverse("admin:agency_newspaper_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.newspaper.title)
        self.assertContains(response, self.newspaper.topic.name)

    def test_topic_list(self):
        url = reverse("admin:agency_topic_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.topic.name)
