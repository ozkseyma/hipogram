from django.contrib import admin
from .models import Post, Tag, Like, Rate

admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Rate)


class PostAdmin(admin.ModelAdmin):
    list_display = ("created_by", "creation_datetime", "_tags")
    list_filter = ("created_by", "tags")

    def _tags(self, post):
        return list(post.tags.all())


admin.site.register(Post, PostAdmin)
