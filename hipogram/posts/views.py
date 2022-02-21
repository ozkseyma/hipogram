from django.views.generic import ListView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponseRedirect


from .models import Post, Tag, Like, Rate
from .forms import PostForm, RatePostForm


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


"""
class ShareView(CreateView):
    model = Post
    fields = ['image', 'text', 'created_by', 'tags', 'creation_datetime']
    template_name = "share.html"
    form = 'PostForm'
"""


@login_required()
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect("posts:list")
    else:
        form = PostForm()
    return render(request, 'share.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.created_by:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            post.delete()
            messages.success(request, 'You have successfully deleted the post')
            return redirect("posts:list")
        else:
            form = PostForm(instance=post)

        return render(request, "delete.html", {'form': form})
    else:
        messages.error(request, 'You are not the owner of this post, please log in.')
        return redirect("users:login")


def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.created_by:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully updated the post')
                return redirect("posts:list")
        else:
            form = PostForm(instance=post)

        return render(request, "update.html", {'form': form, 'post': post})
    else:
        messages.error(request, 'You are not the owner of this post, please log in.')
        return redirect("users:login")


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


"""
#option 2 to update a post
class update_post(UpdateView):
    model = Post
    fields = ['text', 'tags']
    template_name = 'update.html'
    form = 'PostForm'
    success_url = "list"
"""
