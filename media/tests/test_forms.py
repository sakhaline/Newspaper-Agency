from django.test import TestCase
from django.contrib.auth import get_user_model
from media.forms import (TopicSearchForm,
                         RedactorSearchForm,
                         RedactorCreationForm,
                         RedactorUpdateForm,)


class FormsTest(TestCase):
    def test_topic_search_form(self):
        form_data = {
            'topic_name': 'Test Topic',
        }
        form = TopicSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_search_form(self):
        form_data = {
            'search_query': 'Test',
        }
        form = RedactorSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_creation_form(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'years_of_experience': 3,
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_update_form(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Test',
            last_name='User',
            email='test@example.com',
        )
        form_data = {
            'username': 'newusername',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'years_of_experience': 5,
        }
        form = RedactorUpdateForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())
