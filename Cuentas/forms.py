import logging

from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    BaseUserCreationForm,
)
from django import forms
from Cuentas.models import Alumno, Profesor, CustomUser


class CustomAuthForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Email Address"}
        )
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password"}),
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
    }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.username_field.verbose_name},
                )
            try:
                self.confirm_login_allowed(self.user_cache)
            except forms.ValidationError:
                print("User is not allowed to login")

        return self.cleaned_data

    class Meta:
        model = CustomUser
        fields = ("email", "password")


class CustomUserCreationForm(BaseUserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "last_name", "is_student", "is_teacher")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "last_name", "is_student", "is_teacher")
        field_classes = {"email": forms.EmailField}
