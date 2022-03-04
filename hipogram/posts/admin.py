from django.contrib import admin
from .models import Post, Tag, Like, Rate
from django.contrib.auth.models import User
from hipogram.core.mixins import ReadOnlyAdminMixin

admin.site.register(Tag)
admin.site.unregister(User)


class LikeInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Like


class RateInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Rate


class PostInline(admin.TabularInline):
    model = Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("created_by", "creation_datetime", "_tags")
    list_filter = ("created_by", "tags")
    inlines = [LikeInline, RateInline]

    def _tags(self, post):
        return list(post.tags.all())


@admin.register(Like)
class LikeAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_filter = ("post", "user")
    list_display = ("post", "user")


@admin.register(Rate)
class RateAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_filter = ("post", "user")
    list_display = ("post", "user", "value")


@admin.register(User)
class UserAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("username", "first_name", "email", "is_active", "is_staff")
    inlines = [PostInline]
