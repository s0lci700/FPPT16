from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# Create your models here.
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        if not email:
            raise ValueError("El email debe ser obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not extra_fields.get("is_superuser", False):
            raise ValueError("Superuser must have is_superuser=True.")
        if not extra_fields.get("is_staff", False):
            raise ValueError("Superuser must have is_staff=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(
        upload_to="media/perfiles/profile_pictures",
        default="Perfiles/static/default.png",
        blank=True,
    )
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(
        max_length=50, blank=True, verbose_name="Nombre", help_text="Nombre del usuario"
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Apellido",
        help_text="Apellido del usuario",
    )
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # other properties
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    avatar = models.ImageField(
        upload_to="media/perfiles/profile_pictures",
        default="Perfiles/static/default.png",
        blank=True,
    )

    class Meta:
        db_table = "CustomUser"

    def __str__(self):
        return f"Custom User: {self.first_name} {self.last_name}"


class Alumno(CustomUser):
    year_choices = [("3", "3"), ("4", "4")]
    year = models.CharField(max_length=1, choices=year_choices, blank=True)

    def save(self, *args, **kwargs):
        self.is_student = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Alumne:{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Alumne"
        verbose_name_plural = "Alumnes"
        db_table = "Alumno"


class Profesor(CustomUser):
    def save(self, *args, **kwargs):
        self.is_teacher = True
        super().save(*args, **kwargs)

    def __str__(self):
        return "Prof. " + self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        db_table = "Profesor"
