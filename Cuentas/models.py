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
    ROLE_CHOICES = (
        ("A", "Alumno"),
        ("P", "Profesor"),
        ("NS", "No especificado"),
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default="NS",
        verbose_name="Rol",
        help_text="Rol del usuario",
    )
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

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

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.role}: {self.first_name + ' ' + self.last_name}"

    class Meta:
        ordering = ["last_name", "first_name", 'role']


class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'A'},
        related_name="studentprofile"
    )
    year_choices = [('3', "3"), ('4', "4")]
    year = models.CharField(max_length=1, choices=year_choices, blank=True)


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'P'},
        related_name="teacherprofile",
    )