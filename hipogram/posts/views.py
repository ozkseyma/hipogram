from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView

from .models import Post

from taggit.models import Tag
from .forms import PostForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

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
    form = 'PostForm'
"""
#to create a new post
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect("list")
    else:
        form = PostForm()
    return render(request, 'share.html', {'form': form})
    
#to delete a post
def delete_post(request, pk):
    template_name = 'update.html'
    post = get_object_or_404(Post, pk=pk)

    try:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            post.delete()
            messages.success(request, 'You have successfully deleted the post')
        else:
            form = PostForm(instance=post)
    except Exception as e:
        messages.warning(request, 'The post could not be deleted: Error {}'.format(e))

    context = {'form':form,}

    return render(request, template_name, context)

#to update a post
def update_post(request, id):
    context = {}
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST, instance=post)

    #save the data from the form
    if form.is_valid():
        form.save()
        return redirect("list")

    # add form dictionary to context
    context["form"] = form

    return render(request, "update.html", context)
"""
#option 2 to update a post
class update_post(UpdateView):
    model = Post
    fields = ['text', 'tags']
    template_name = 'update.html'
    form = 'PostForm'
    success_url = "list"
"""