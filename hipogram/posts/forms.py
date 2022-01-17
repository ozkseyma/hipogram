from django import forms

from .models import Post

#in order to create posts
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('image', 'text', 'tags',)   