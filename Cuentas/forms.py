from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from Cuentas.models import Alumno, Profesor, CustomUser


class CustomAuthForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", 'password')


class AlumnoCreationForm(CustomUserCreationForm):
    class Meta:
        model = Alumno
        is_student = True
        is_teacher = False
        fields = CustomUserCreationForm.Meta.fields


class ProfesorCreationForm(CustomUserCreationForm):
    class Meta:
        model = Profesor
        is_teacher = True
        is_student = False
        fields = CustomUserCreationForm.Meta.fields
