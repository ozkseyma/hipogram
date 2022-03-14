from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
# from hipogram.posts.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .forms import EditUserForm
from .models import Message


class SignUpView(SuccessMessageMixin, CreateView):
    model = get_user_model()
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
    model = get_user_model()
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
    fields = ["text"]
    template_name = "messages.html"
    pk_url_kwargs = "receiver_id"
    success_url = reverse_lazy("users:messages_list")

    # determine the sender & the receiver of the message
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.sender = self.request.user
        form.instance.receiver_id = self.kwargs["receiver_id"]
        return form

    # show message history of the two users
    def get_context_data(self):
        context = super().get_context_data()
        qs1 = Message.objects.filter(
            sender=self.request.user,
            receiver_id=self.kwargs["receiver_id"]
        )
        qs2 = Message.objects.filter(
            sender_id=self.kwargs["receiver_id"],
            receiver=self.request.user
        )
        context["qs"] = (qs1 | qs2).order_by("creation_datetime")
        return context


class ListMessagesView(ListView):
    model = Message
    context_object_name = "message_list"
    ordering = "-creation_datetime"
    template_name = "list_messages.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            sender=self.request.user
        ).values("receiver__username", "receiver__id").annotate(
            Count("receiver")
        ).order_by("receiver__count")
