from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    PermissionsMixin,
)


# Create your models here.
class CustomUser(AbstractUser):
    ALUMNO = "A"
    PROFESOR = "P"
    NO_ESPECIFICADO = "NS"
    ROLE_CHOICES = (
        (ALUMNO, "Alumno"),
        (PROFESOR, "Profesor"),
        (NO_ESPECIFICADO, "No especificado"),
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default="NS",
        verbose_name="Rol",
        help_text="Rol del usuario",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico",
        help_text="Correo electrónico del usuario",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['role']

    first_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Nombre",
        help_text="Nombre del usuario"
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Apellido",
        help_text="Apellido del usuario",
    )
    avatar = models.ImageField(
        upload_to="perfiles/avatars",
        default="perfiles/default.png",
        blank=True,
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de nacimiento",
        help_text="Fecha de nacimiento del usuario",
    )

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name + ' ' + self.last_name}"

    class Meta:
        ordering = ["last_name", "first_name", 'role']
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'A'},
        related_name="studentprofile"
    )
    TERCERO = "3"
    CUARTO = "4"
    year_choices = [
        (TERCERO, "Tercer Año"),
        (CUARTO, "Cuarto Año"),
    ]
    year = models.CharField(choices=year_choices, max_length=1, default="3")

    def __str__(self):
        return f"Alumne: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Perfil de alumno"
        verbose_name_plural = "Perfiles de alumnos"



class TeacherProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'P'},
        related_name="teacherprofile",
    )

    def __str__(self):
        return f"Profesor: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Perfil de profesor"
        verbose_name_plural = "Perfiles de profesores"
