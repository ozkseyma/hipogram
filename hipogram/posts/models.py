from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager

class Post(models.Model):
    image = models.ImageField()
    text = models.TextField()
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    #like_count = models.IntegerField(default=0)
    #tags = TaggableManager()
    