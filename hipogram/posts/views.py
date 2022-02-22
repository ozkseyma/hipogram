from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


from .models import Post, Tag, Like, Rate
from .forms import RatePostForm


class PostListView(ListView):
    model = Post
    ordering = "-creation_datetime"
    context_object_name = "posts"
    template_name = "post_list.html"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        if username := self.request.GET.get('username'):
            queryset = queryset.filter(created_by__username=username)
        if tag := self.request.GET.get('tag'):
            queryset = queryset.filter(tags__name=tag)

        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        today = timezone.now().date()

        context['tags'] = Tag.objects.filter(
            post__creation_datetime__date=today
        ).annotate(Count('post')).order_by('-post__count')
        context['form'] = RatePostForm()
        return context


class PostCreateView(CreateView):
    model = Post
    fields = ['image', 'text', 'tags']
    template_name = "share.html"
    success_url = reverse_lazy("posts:list")
    pk_url_kwarg = 'post_id'

    # override this method to determine the creator of the post
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.created_by = request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy("posts:list")
    pk_url_kwarg = 'post_id'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['text', 'tags']
    context_object_name = "post"
    template_name = "update.html"
    success_url = reverse_lazy("posts:list")
    pk_url_kwarg = 'post_id'


@login_required()
def like_post(request, post_id):
    like, created = Like.objects.get_or_create(user=request.user, post_id=post_id)

    if not created:
        like.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def rate_post(request, post_id):

    if request.method == 'POST':
        form = RatePostForm(request.POST)

    # if not form.is_valid():
        # do something

        rate, _ = Rate.objects.get_or_create(user=request.user, post_id=post_id)
        rate.value = form.data['value']
        rate.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
