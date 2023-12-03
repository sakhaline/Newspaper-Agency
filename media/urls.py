from django.urls import path

from media.views import (IndexView,
                         TopicListView,
                         NewspaperListView,
                         RedactorListView,
                         NewspaperDetailView,
                         RedactorDetailView,
                         NewspaperCreateView,
                         NewspaperUpdateView,
                         NewspaperDeleteView,
                         TopicCreateView,
                         TopicUpdateView,
                         TopicDeleteView,
                         RedactorRegisterView,
                         RedactorUpdateView)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topic/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topic/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),
    path("topic/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),

    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspapers/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path('newspapers/by-topic/<str:topic_name>/', NewspaperListView.as_view(), name='newspaper-list-by-topic'),

    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path("register/", RedactorRegisterView.as_view(), name="redactor-form"),
    path("redactors/<int:pk>/update", RedactorUpdateView.as_view(), name="redactor-form"),
    path("accounts/sign_up/", RedactorRegisterView.as_view(), name="sign-up")
]


app_name = "media"
