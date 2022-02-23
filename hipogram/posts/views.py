from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Post, Tag, Like, Rate
from .forms import RatePostForm
from .mixins import OwnerRequiredMixin


class PostListView(ListView):
    model = Post
    ordering = "-creation_datetime"
    context_object_name = "posts"
    template_name = "post_list.html"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        if username := self.request.GET.get("username"):
            queryset = queryset.filter(created_by__username=username)
        if tag := self.request.GET.get("tag"):
            queryset = queryset.filter(tags__name=tag)

        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        today = timezone.now().date()

        context["tags"] = Tag.objects.filter(
            post__creation_datetime__date=today
        ).annotate(Count("post")).order_by("-post__count")
        context["form"] = RatePostForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["image", "text", "tags"]
    template_name = "share.html"
    success_url = reverse_lazy("posts:list")
    pk_url_kwarg = "post_id"

    # determine the creator of the post
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.created_by = self.request.user
        return form


class PostDeleteView(OwnerRequiredMixin, DeleteView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy("posts:list")
    pk_url_kwarg = "post_id"


class PostUpdateView(OwnerRequiredMixin, UpdateView):
    model = Post
    fields = ["text", "tags"]
    context_object_name = "post"
    template_name = "update.html"
    success_url = reverse_lazy("posts:list")
    pk_url_kwarg = "post_id"


class LikeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        like, created = Like.objects.get_or_create(user=request.user, post_id=kwargs["post_id"])

        if not created:
            like.delete()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class RateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        form = RatePostForm(request.POST)
        rate, _ = Rate.objects.get_or_create(user=request.user, post_id=kwargs["post_id"])
        rate.value = form.data["value"]
        rate.save()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
