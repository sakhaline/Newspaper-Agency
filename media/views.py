from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from media.models import Redactor, Newspaper, Topic
from media.forms import NewspaperCreationForm

@login_required
def index(request):
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "media/index.html", context=context)


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.all().select_related("topic")


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperCreateView(generic.CreateView):
    form_class = NewspaperCreationForm
    template_name = "media/newspaper_form.html"
    success_url = reverse_lazy("media:newspaper-list")


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("media:newspaper-list")


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("media:newspaper-list")


class RedactorListView(generic.ListView):
    model = Redactor


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers")


class TopicListView(generic.ListView):
    model = Topic


class TopicCreateView(generic.CreateView):
    model = Topic
    fields = "__all__"
    template_name = "media/topic_form.html"
    success_url = reverse_lazy("media:topic-list")


class TopicUpdateView(generic.UpdateView):
    model = Topic
    fields = "__all__"
    template_name = "media/topic_form.html"
    success_url = reverse_lazy("media:topic-list")


class TopicDeleteView(generic.DeleteView):
    model = Topic
    fields = "__all__"
    template_name = "media/topic_confirm_delete.html"
    success_url = reverse_lazy("media:topic-list")