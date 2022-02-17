from django import forms

from .models import Post, Rate


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'text', 'tags', ]


class RatePostForm(forms.ModelForm):

    class Meta:
        model = Rate
        fields = ['value']
