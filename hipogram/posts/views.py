from django.views.generic import ListView
from django.views.generic import CreateView

from .models import Post

from taggit.models import Tag
from .forms import PostForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone


class PostListView(ListView):
    model = Post
    ordering = "-creation_datetime"
    context_object_name = "posts"
    template_name = "post_list.html"

"""
class ShareView(CreateView):
    model = Post
    fields = ['image', 'text', 'created_by', 'tags', 'creation_datetime']
    template_name = "share.html"
    context_object_name = "posts"
"""
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect("post_list")
    else:
        form = PostForm()
    return render(request, 'share.html', {'form': form})