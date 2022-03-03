from django.contrib import admin
from .models import Post, Tag, Like, Rate
from django.contrib.auth.models import User
from hipogram.core.mixins import ReadOnlyAdminMixin


class LikeInline(admin.TabularInline):
    model = Like


class RateInline(admin.TabularInline):
    model = Rate


class PostInline(admin.TabularInline):
    model = Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("created_by", "creation_datetime", "_tags")
    list_filter = ("created_by", "tags")
    inlines = [LikeInline, RateInline]

    def _tags(self, post):
        return list(post.tags.all())


class LikeAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_filter = ("post", "user")
    list_display = ("post", "user")


class RateAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_filter = ("post", "user")
    list_display = ("post", "user", "value")


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "email", "is_active", "is_staff")
    inlines = [PostInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tag)
