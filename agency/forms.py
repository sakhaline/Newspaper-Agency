from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from agency.models import Newspaper, Topic


class NewspaperCreationForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class NewspaperFilterForm(forms.Form):
    topic_name = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        empty_label="All topics",
        required=False,
    )


class NewspaperSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title..."})
    )


class TopicSearchForm(forms.Form):
    topic_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )


class RedactorSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search..."})
    )


class RedactorRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        )
        help_text = {"username": ""}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = ""


class RedactorUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        )
