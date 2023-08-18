import logging

from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    BaseUserCreationForm,
)
from django import forms
from Cuentas.models import CustomUser


class CustomAuthForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Email Address"}
        )
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
    }

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                    params={"email": self.username_field.verbose_name},
                )
            try:
                self.confirm_login_allowed(self.user_cache)
            except forms.ValidationError:
                logging.error("User is not allowed to login")

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ("email", "password")


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={"placeholder": "Role"}),
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"placeholder": "Avatar"}),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2", "first_name", "last_name", "role", "avatar")
        widgets = {
            "username": forms.EmailInput(attrs={"placeholder": "Email Address"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Password"}),
            "password2": forms.PasswordInput(
                attrs={"placeholder": "Password Confirmation"}
            ),
        }


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={"placeholder": "Role"}),
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"placeholder": "Avatar"}),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name", "last_name", "role", "avatar")
