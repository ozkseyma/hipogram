from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView


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


class LogInView(SuccessMessageMixin, DjangoLoginView):
    success_message = "You are successfully logged in!"
    template_name = "login.html"


class LogOutView(SuccessMessageMixin, DjangoLogoutView):
    success_message = "You are successfully logged out!"
