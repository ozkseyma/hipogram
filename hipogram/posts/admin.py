from django.contrib import admin
from .models import Post, Tag

admin.site.register(Tag)


class PostAdmin(admin.ModelAdmin):
    list_display = ("created_by", "creation_datetime", "Tags")
    list_filter = ("created_by", "tags")

    def Tags(self, obj):
        queryset = []
        for tag in obj.tags.all():
            queryset.append(tag)
        return queryset


admin.site.register(Post, PostAdmin)
