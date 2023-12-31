from django.db import models
from django.utils import timezone
from datetime import datetime
from taggit.managers import TaggableManager
import os
from embed_video.fields import EmbedVideoField


def upload_to(instance, filename):
    return os.path.join(
        "student",
        str(instance.student.id),
        "ficha",
        str(instance.id),
        "images",
        filename,
    )


# Create your models here.
imgChoices = (
    ("MAIN", "main"),
    ("FOTO", "fotograma"),
    ("COMP", "complementaria"),
    ("REF", "referencia"),
    ("O", "otra"),
)


class FichaImage(models.Model):
    ficha = models.ForeignKey("Ficha", on_delete=models.CASCADE, related_name="images")
    student = models.ForeignKey("Cuentas.StudentProfile", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to)
    attributes = models.CharField(
        max_length=20,
        choices=imgChoices,
    )

    def __str__(self):
        return self.ficha.title + " - " + self.image.name


def get_default_start_date():
    return timezone.now().date()


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    time_window_start = models.DateField(default=get_default_start_date)
    time_window_end = models.DateField()

    def is_open(self):
        current_datetime = timezone.now().date()

        if self.time_window_start is None or self.time_window_end is None:
            return False

        return self.time_window_start <= current_datetime <= self.time_window_end

    @property
    def status(self):
        return "OPEN" if self.is_open() else "CLOSED"

    def __str__(self):
        return self.title


class Ficha(models.Model):
    STATUS_CHOICES = (
        ("Borrador", "Borrador"),
        ("Publicado", "Publicado"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Borrador")
    student = models.ForeignKey(
        "Cuentas.StudentProfile",
        on_delete=models.CASCADE,
        related_query_name="fichas",
        related_name="user_ficha",
    )
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="fichas"
    )
    title = models.CharField(max_length=50)
    main_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    description = models.TextField(blank=True)
    analysis = models.TextField(blank=True)
    references = models.TextField(blank=True)
    keywords = TaggableManager(blank=True)
    anexos = EmbedVideoField(blank=True)
    misc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def linked_assignment_id(self):
        return self.assignment.id

    def anexos_as_list(self):
        return self.anexos.split(",")

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ("student", "assignment")


class Review(models.Model):
    teacher = models.ForeignKey("Cuentas.TeacherProfile", on_delete=models.CASCADE)
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("teacher", "ficha")

    def __str__(self):
        return f"{self.ficha.title} reseñado por {self.teacher.user.first_name}"
