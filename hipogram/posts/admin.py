from django.contrib import admin
from .models import Post, Tag

admin.site.register(Tag)


class PostAdmin(admin.ModelAdmin):
    list_display = ("created_by", "creation_datetime", "_tags")
    list_filter = ("created_by", "tags")

    def _tags(self, post):
        return list(post.tags.all())


admin.site.register(Post, PostAdmin)
