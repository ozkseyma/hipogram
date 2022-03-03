from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.forms import PasswordInput


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "password"]

        widgets = {
            "password": PasswordInput(attrs={"placeholder": ""}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["username"].required = False
        self.fields["password"].required = False

    def clean_password(self):
        if self.cleaned_data["password"]:
            password_validation.validate_password(self.cleaned_data["password"], self.user)
