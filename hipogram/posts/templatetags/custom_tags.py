from django import template

register = template.Library()


@register.simple_tag
def is_liked(post, user):
    return user.is_authenticated and post.likes.filter(post=post, user=user).exists()
