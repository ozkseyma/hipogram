from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#from taggit.models import Tag

from .models import Post
from .forms import PostForm, PostForm2


class PostListView(ListView):
    model = Post
    ordering = "-creation_datetime"
    context_object_name = "posts"
    template_name = "post_list.html"
    paginate_by = 2

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
            post=form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect("posts:list")
    else:
        form = PostForm()
    return render(request, 'share.html', {'form': form})
    
@login_required()
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            post.delete()
            messages.success(request, 'You have successfully deleted the post')
            return redirect("posts:list")
        else:
            form = PostForm(instance=post)

        return render(request, "delete.html", {'form':form})
    else:
        return redirect("user:login")

@login_required()
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm2(request.POST, instance=post)

    #save the data from the form
    if request.user.is_authenticated:
        if form.is_valid():
            form.save()
            return redirect("posts:list")

        return render(request, "update.html", {'form':form})
    else:
        return redirect("user:login")     
"""
#option 2 to update a post
class update_post(UpdateView):
    model = Post
    fields = ['text', 'tags']
    template_name = 'update.html'
    form = 'PostForm'
    success_url = "list"
"""