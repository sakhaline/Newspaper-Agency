from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.db.models import Q, QuerySet

from media.models import Redactor, Newspaper, Topic
from media.forms import (NewspaperCreationForm,
                         NewspaperFilterForm,
                         TopicSearchForm,
                         RedactorSearchForm,
                         RedactorCreationForm,
                         RedactorUpdateForm,)


@login_required
def index(request: HttpRequest) -> HttpResponse:
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
    paginate_by = 5

    def get_queryset(self):
        form = NewspaperFilterForm(self.request.GET)

        queryset = Newspaper.objects.all()

        if form.is_valid():
            topic_name = form.cleaned_data.get('topic_name')
            query_search = form.cleaned_data.get('query_search')

            if topic_name:
                queryset = queryset.filter(topic=topic_name)

            if query_search:
                queryset = queryset.filter(
                    Q(title__icontains=query_search)
                    | Q(content__icontains=query_search)
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewspaperFilterForm(self.request.GET)
        return context


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = NewspaperCreationForm
    template_name = "media/newspaper_form.html"
    success_url = reverse_lazy("media:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("media:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    fields = "__all__"
    template_name = "media/newspaper_confirm_delete.html"
    success_url = reverse_lazy("media:newspaper-list")


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers")


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 4

    def get_queryset(self) -> QuerySet:
        form = RedactorSearchForm(self.request.GET)
        queryset = Redactor.objects.all()

        if form.is_valid():
            search_value = form.cleaned_data.get("search_query")

            return queryset.filter(
                (
                    Q(username__icontains=search_value)
                    | Q(first_name__icontains=search_value)
                    | Q(last_name__icontains=search_value)
                )
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = RedactorSearchForm(self.request.GET)
        return context


class RedactorCreationView(generic.CreateView):
    form_class = RedactorCreationForm
    template_name = 'registration/register.html'

    def get_success_url(self) -> str:
        return self.request.GET.get("next", "/")

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = RedactorUpdateForm
    template_name = "media/redactor_form.html"
    queryset = Redactor.objects.all()

    def get_success_url(self) -> str:
        return reverse_lazy("media:redactor-list")


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 4

    def get_queryset(self) -> QuerySet:
        form = TopicSearchForm(self.request.GET)
        queryset = Topic.objects.all()

        if form.is_valid():
            topic_name = form.cleaned_data.get('topic_name')
            return queryset.filter(name__icontains=topic_name)

        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['form'] = TopicSearchForm(self.request.GET)
        return context


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    template_name = "media/topic_form.html"
    success_url = reverse_lazy("media:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    template_name = "media/topic_form.html"
    success_url = reverse_lazy("media:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    fields = "__all__"
    template_name = "media/topic_confirm_delete.html"
    success_url = reverse_lazy("media:topic-list")
