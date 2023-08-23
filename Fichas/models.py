from django.db import models
from taggit.managers import TaggableManager


# Create your models here.


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
    title = models.CharField(max_length=50)
    main_image = models.ImageField(upload_to="fichas/images/", blank=True, null=True)
    description = models.TextField(blank=True)
    analysis = models.TextField(blank=True)
    references = models.TextField(blank=True)
    keywords = TaggableManager(blank=True)
    misc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ComplementaryImage(models.Model):
    ficha = models.ForeignKey(
        Ficha, on_delete=models.CASCADE, related_name="complementary_images"
    )
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.ficha.title + " - " + self.image.name


class Keywords(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Review(models.Model):
    teacher = models.ForeignKey("Cuentas.TeacherProfile", on_delete=models.CASCADE)
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ficha.title
