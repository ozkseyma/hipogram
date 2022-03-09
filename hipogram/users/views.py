from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView


from .forms import EditUserForm
from .models import Message


class SignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("posts:list")
    success_message = "You are succesfully signed up!"

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)

        return valid


class LogInView(SuccessMessageMixin, LoginView):
    success_message = "You are successfully logged in!"
    template_name = "login.html"


class LogOutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'You are successfully logged out.')
        return super().dispatch(request, *args, **kwargs)


class EditProfileView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = "edit.html"
    pk_url_kwarg = "user_id"
    success_url = reverse_lazy("posts:list")
    success_message = "You have successfully edited your profile!"

    def get_form_kwargs(self):
        return {
            "user": self.request.user,
            **super().get_form_kwargs()
        }

    def form_valid(self, form):
        if form.data["password"]:
            self.request.user.set_password(form.data["password"])

        if form.data["username"]:
            self.request.user.username = form.data["username"]
            self.request.user.save()

        login(self.request, self.request.user)
        return redirect("posts:list")


class MessagesView(CreateView):
    model = Message
    fields = ["receiver", "text"]
    template_name = "messages.html"
    pk_url_kwargs = "user_id"
    success_url = reverse_lazy("users:message")

    def get_context_data(self):
        context = super().get_context_data()
        context["message_history"] = Message.objects.filter(
            sender__id=self.kwargs["user_id"],
        )
        return context


class ListMessagesView(ListView):
    model = Message
    context_object_name = "messages"
    ordering = "-creation_datetime"
    template_name = "list_messages.html"

    def get_queryset(self):
        return super().get_queryset().filter(sender__id=self.kwargs["user_id"])
