from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='perfiles/profile_pictures', blank=True, default='default.png')
    pronouns = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    class Meta:
        db_table = "AbstractUser or Admin"


class Alumno(CustomUser):
    is_student = True
    year_choices = [('3', '3'), ('4', '4')]
    year = models.CharField(max_length=1, choices=year_choices, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name_plural = "Alumnos"
        db_table = "Alumno"


class Profesor(CustomUser):
    is_teacher = True

    def __str__(self):
        return 'Prof. ' + self.first_name + " " + self.last_name

    class Meta:
        verbose_name_plural = "Profesores"
        db_table = "Profesor"
