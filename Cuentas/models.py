from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"

    first_name = models.CharField(
        max_length=50, blank=True, verbose_name="Nombre", help_text="Nombre del usuario"
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Apellido",
        help_text="Apellido del usuario",
    )
    ROLE_CHOICES = (
        ("A", "Alumno"),
        ("P", "Profesor"),
        ("NS", "No especificado"),
    )
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default="NS")

    avatar = models.ImageField(
        upload_to="media/perfiles/profile_pictures",
        default="media/perfiles/default.png",
        blank=True,
    )

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def is_student(self):
        return hasattr(self, "studentprofile")

    @property
    def is_teacher(self):
        return hasattr(self, "teacherprofile")

    def __str__(self):
        return f"Custom User: {self.email}"

    class Meta:
        db_table = "CustomUser"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def save(self, *args, **kwargs):
        if hasattr(self, "studentprofile"):
            self.role = "A"
        elif hasattr(self, "teacherprofile"):
            self.role = "P"
        else:
            self.role = "NS"
        super().save(*args, **kwargs)


class StudentProfile(models.Model):
    userprofile = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="studentprofile"
    )
    year_choices = [('3', "3"), ('4', "4")]
    year = models.CharField(max_length=1, choices=year_choices, blank=True)


class TeacherProfile(models.Model):
    userprofile = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="teacherprofile"
    )


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "A":
            StudentProfile.objects.create(userprofile=instance)
        elif instance.role == "P":
            TeacherProfile.objects.create(userprofile=instance)
        else:
            pass


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == "A" and hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()
    elif instance.role == "P" and hasattr(instance, 'teacherprofile'):
        instance.teacherprofile.save()