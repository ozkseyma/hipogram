from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        post = self.get_object()
        if post.created_by != self.request.user:
            return self.handle_no_permission()
        return response
