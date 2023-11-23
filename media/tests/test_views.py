from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from newspaper.models import Newspaper, Topic


class PublicNewspaperTests(TestCase):

    def setUp(self) -> None:
        topic = Topic.objects.create(name="testT")
        self.newspaper = Newspaper.objects.create(
            title="test_t",
            content="etesd",
            topic=topic,
        )

    def test_login_not_required(self):
        url = reverse("newspaper:newspaper-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        urls = [
            reverse("newspaper:newspaper-detail", args=[self.newspaper.id]),
            reverse("newspaper:newspaper-update", args=[self.newspaper.id]),
            reverse("newspaper:newspaper-delete", args=[self.newspaper.id]),
            reverse("newspaper:newspaper-create")
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateNewspaperTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)

        self.topic = Topic.objects.create(name="Test Topic")
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            topic=self.topic
        )

    def test_newspaper_list_view(self):
        url = reverse("newspaper:newspaper-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_newspaper_detail_view(self):
        url = reverse("newspaper:newspaper-detail", args=[self.newspaper.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add more specific assertions based on your expectations for the detail view

    def test_newspaper_create_view(self):
        url = reverse("newspaper:newspaper-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_newspaper_update_view(self):
        url = reverse("newspaper:newspaper-update", args=[self.newspaper.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_newspaper_delete_view(self):
        url = reverse("newspaper:newspaper-delete", args=[self.newspaper.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_newspaper_list_search(self):
        url = reverse("newspaper:newspaper-list")
        response = self.client.get(url, {"title": "Test Newspaper"})
        self.assertEqual(response.status_code, 200)

    def test_redactor_list_view(self):
        url = reverse("newspaper:redactor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_redactor_detail_view(self):
        redactor = get_user_model().objects.create(username="test_redactor")
        url = reverse("newspaper:redactor-detail", args=[redactor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_topic_list_view(self):
        url = reverse("newspaper:topic-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_topic_detail_view(self):
        url = reverse("newspaper:topic-detail", args=[self.topic.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_redactor_create_view(self):
        url = reverse("newspaper:redactor-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        def test_redactor_update_view(self):
            redactor = get_user_model().objects.create(username="test_redactor")
            url = reverse("newspaper:redactor-update", args=[redactor.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_redactor_delete_view(self):
            redactor = get_user_model().objects.create(username="test_redactor")
            url = reverse("newspaper:redactor-delete", args=[redactor.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_redactor_search_view(self):
            url = reverse("newspaper:redactor-list")
            response = self.client.get(url, {"username": "test_redactor"})
            self.assertEqual(response.status_code, 200)

        def test_topic_create_view(self):
            url = reverse("newspaper:topic-create")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_topic_update_view(self):
            url = reverse("newspaper:topic-update", args=[self.topic.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_topic_delete_view(self):
            topic = Topic.objects.create(name="test_topic")
            url = reverse("newspaper:topic-delete", args=[topic.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_topic_search_view(self):
            url = reverse("newspaper:topic-list")
            response = self.client.get(url, {"name": "test_topic"})
            self.assertEqual(response.status_code, 200)

class TopicTests(TestCase):
    def test_retrieve_topic_list(self):
        Topic.objects.create(name="test_topic1")
        Topic.objects.create(name="test_topic2")

        response = self.client.get(reverse("newspaper:topic-list"))

        topics = Topic.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics)
        )
        self.assertTemplateUsed(response, "newspaper/topic_list.html")

    def test_topic_list_search(self):
        Topic.objects.create(name="test_topic")
        Topic.objects.create(name="Science")
        response = self.client.get(reverse("newspaper:topic-list"), {"name": "test_topic"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(Topic.objects.filter(name="test_topic"))
        )