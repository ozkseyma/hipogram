from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "password"]

        widgets = {
            "password": PasswordInput(attrs={'placeholder': '', 'autocomplete': 'off'}),
        }
