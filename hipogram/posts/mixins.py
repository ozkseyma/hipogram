from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect


class OwnerRequiredMixin(DjangoLoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.created_by != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, "You are not the owner of this post!")
        return redirect("users:login")


class LoginRequiredMixin(DjangoLoginRequiredMixin):

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, "You are not logged in!")
        return redirect("users:login")


class ReadOnlyAdminMixin:

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
