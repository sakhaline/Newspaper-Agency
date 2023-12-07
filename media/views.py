from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect,
)

from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q, QuerySet

from media.models import Redactor, Newspaper, Topic
from media.forms import (
    NewspaperCreationForm,
    NewspaperFilterForm,
    NewspaperSearchForm,
    TopicSearchForm,
    RedactorSearchForm,
    RedactorRegisterForm,
    RedactorUpdateForm,
)


@login_required
def delete_newspaper_view(request, pk):
    newspaper = get_object_or_404(Newspaper, pk=pk)

    if (
        request.user.groups.filter(name="Mod").exists()
        or request.user == newspaper.publishers.first()
    ):
        if request.method == "POST":
            newspaper.delete()
            return redirect("media:newspaper-list")
        else:
            return render(
                request=request,
                template_name="media/newspaper_confirm_delete.html",
                context={"newspaper": newspaper},
            )
    else:
        return HttpResponseForbidden(
            "You don't have permission to delete this newspaper."
        )


class IndexView(generic.TemplateView):
    template_name = "media/index.html"


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.all().select_related("topic")
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
        filter_form = NewspaperFilterForm(self.request.GET)
        search_form = NewspaperSearchForm(self.request.GET)

        queryset = Newspaper.objects.all()

        if filter_form.is_valid():
            topic_name = filter_form.cleaned_data.get("topic_name")

            if topic_name:
                queryset = queryset.filter(topic=topic_name)

        if search_form.is_valid():
            search_query = search_form.cleaned_data.get("search_query")

            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query)
                    | Q(content__icontains=search_query)
                )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["filter_form"] = NewspaperFilterForm(self.request.GET)
        context["search_form"] = NewspaperSearchForm(self.request.GET)

        return context


class NewspaperDetailView(generic.DetailView):
    model = Newspaper

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_in_mod_group"] = self.request.user.groups.filter(
            name="Mod"
        ).exists()

        return context


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


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers")


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 5

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
        context["user_in_admin_group"] = self.request.user.groups.filter(
            name="Admin"
        ).exists()

        return context


class RedactorRegisterView(generic.CreateView):
    form_class = RedactorRegisterForm
    template_name = "registration/sign_up.html"

    def get_success_url(self) -> str:
        return self.request.GET.get("next", "/")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = RedactorUpdateForm
    template_name = "media/redactor_form.html"
    success_url = reverse_lazy("media:redactor-list")

    def get_queryset(self) -> QuerySet:
        return Redactor.objects.filter(id=self.request.user.id)


class RedactorDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = get_user_model()
    queryset = get_user_model().objects.all()
    success_url = reverse_lazy("media:redactor-list")

    permission_required = "media.delete_redactor"


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
        form = TopicSearchForm(self.request.GET)
        queryset = Topic.objects.all()

        if form.is_valid():
            topic_name = form.cleaned_data.get("topic_name")
            return queryset.filter(name__icontains=topic_name)

        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        context["form"] = TopicSearchForm(self.request.GET)
        context["user_in_mod_group"] = self.request.user.groups.filter(
            name="Mod"
        ).exists()

        return context


class TopicCreateView(PermissionRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("media:topic-list")

    permission_required = "media.add_topic"


class TopicUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("media:topic-list")

    permission_required = "media.change_topic"


class TopicDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("media:topic-list")

    permission_required = "media.delete_topic"
