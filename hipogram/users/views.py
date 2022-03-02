from django.contrib import messages
from django.contrib.auth import login, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import EditUserForm


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

    def form_valid(self, form):
        password_validation.validate_password(form.data["password"], self.request.user)
        self.request.user.set_password(form.data["password"])
        self.request.user.username = form.data["username"]
        self.request.user.save()

        return redirect("posts:list")
