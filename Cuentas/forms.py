from django.contrib.auth.forms import UserCreationForm

from Cuentas.models import Alumno, Profesor, CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "is_student", "is_teacher")


class AlumnoForm(CustomUserForm):
    class Meta:
        model = Alumno
        is_student = True
        fields = CustomUserForm.Meta.fields + ("pronouns",)


class ProfesorForm(CustomUserForm):
    class Meta:
        model = Profesor
        is_teacher = True
        fields = CustomUserForm.Meta.fields + ("pronouns",)
