from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q, QuerySet

from media.models import Redactor, Newspaper, Topic
from media.forms import (NewspaperCreationForm,
                         NewspaperFilterForm,
                         TopicSearchForm,
                         RedactorSearchForm,
                         RedactorRegisterForm,
                         RedactorUpdateForm)


class IndexView(generic.TemplateView):
    template_name = "media/index.html"


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.all().select_related("topic").order_by("pk")
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
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

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
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

    def get_queryset(self) -> QuerySet:
        return Newspaper.objects.filter(publishers=self.request.user)


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


class RedactorRegisterView(generic.CreateView):
    form_class = RedactorRegisterForm
    template_name = 'registration/sign_up.html'

    def get_success_url(self) -> str:
        return self.request.GET.get("next", "/")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = RedactorUpdateForm
    template_name = "media/redactor_form.html"
    success_url = reverse_lazy("media:redactor-list")

    def get_queryset(self) -> QuerySet:
        return Redactor.objects.filter(id=self.request.user.id)


class RedactorDeleteView(generic.DeleteView):
    model = get_user_model()
    queryset = get_user_model().objects.all()
    success_url = reverse_lazy("media:redactor-list")


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
    success_url = reverse_lazy("media:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("media:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("media:topic-list")
