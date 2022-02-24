from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.created_by != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
