from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from media.models import Newspaper, Topic, Redactor


class NewspaperViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        cls.topic = Topic.objects.create(name='Test Topic')
        cls.newspaper = Newspaper.objects.create(title='Test Newspaper', content='Lorem ipsum', topic=cls.topic)

    def setUp(self):
        self.client.login(username='testuser', password='testpassword')

    def test_newspaper_list_view(self):
        response = self.client.get(reverse('media:newspaper-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/newspaper_list.html')
        self.assertContains(response, 'Test Newspaper')

    def test_newspaper_detail_view(self):
        response = self.client.get(reverse('media:newspaper-detail', args=[self.newspaper.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/newspaper_detail.html')
        self.assertContains(response, 'Test Newspaper')

    def test_newspaper_create_view(self):
        response = self.client.get(reverse('media:newspaper-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/newspaper_form.html')

    def test_newspaper_update_view(self):
        response = self.client.get(reverse('media:newspaper-update', args=[self.newspaper.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/newspaper_form.html')

    def test_newspaper_delete_view(self):
        response = self.client.get(reverse('media:newspaper-delete', args=[self.newspaper.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/newspaper_confirm_delete.html')

    def test_newspaper_create_view_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('media:newspaper-create'))
        self.assertEqual(response.status_code, 302)


class RedactorViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        cls.topic = Topic.objects.create(name='Test Topic')
        cls.newspaper = Newspaper.objects.create(title='Test Newspaper', content='Lorem ipsum', topic=cls.topic)
        cls.redactor = Redactor.objects.create(
            username='test_redactor',
            first_name='Test',
            last_name='Redactor',
            years_of_experience=3
        )
        cls.redactor.newspapers.add(cls.newspaper)

    def setUp(self):
        self.client.login(username='testuser', password='testpassword')

    def test_redactor_detail_view_newspapers(self):
        response = self.client.get(reverse('media:redactor-detail', args=[self.redactor.id]))
        self.assertContains(response, 'Test Newspaper')


class TopicViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        cls.topic = Topic.objects.create(name='Test Topic')
        cls.newspaper = Newspaper.objects.create(title='Test Newspaper', content='Lorem ipsum', topic=cls.topic)
        cls.redactor = Redactor.objects.create(
            username='test_redactor',
            first_name='Test',
            last_name='Redactor',
            years_of_experience=3
        )
        cls.redactor.newspapers.add(cls.newspaper)

    def setUp(self):
        self.client.login(username='testuser', password='testpassword')

    def test_topic_list_view(self):
        response = self.client.get(reverse('media:topic-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/topic_list.html')
        self.assertContains(response, 'Test Topic')

    def test_topic_create_view(self):
        response = self.client.get(reverse('media:topic-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/topic_form.html')

    def test_topic_update_view(self):
        response = self.client.get(reverse('media:topic-update', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/topic_form.html')

    def test_topic_delete_view(self):
        response = self.client.get(reverse('media:topic-delete', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/topic_confirm_delete.html')

    def test_topic_create_view_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('media:topic-create'))
        self.assertEqual(response.status_code, 302)


