from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    image = models.ImageField()
    text = models.TextField()
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, help_text="Ctrl + click to select multiple", blank=True)

    def __str__(self):
        return self.created_by.username

    @property
    def like_count(self):
        Like.objects.filter(post=self).count()


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    like_datetime = models.DateTimeField(auto_now_add=True)
