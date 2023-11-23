from django import forms
from django.contrib.auth import get_user_model

from media.models import Newspaper, Topic


class NewspaperCreationForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
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
    title = forms.CharField(
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
        widget=forms.TextInput(attrs={"placeholder": "Search by username or by first name..."})
    )
