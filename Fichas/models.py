from django.db import models


# Create your models here.


class Ficha(models.Model):
    student = models.ForeignKey('Cuentas.Alumno', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    main_image = models.ImageField(upload_to='images/')
    complementary_images = models.ImageField(upload_to='images/', blank=True)
    description = models.TextField()
    analysis = models.TextField()
    references = models.TextField()
    keywords = models.TextField()
    misc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " - " + self.student.first_name + " " + self.student.last_name


class Review(models.Model):
    teacher = models.ForeignKey('Cuentas.Profesor', on_delete=models.CASCADE)
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ficha.title + " - " + self.teacher.first_name + " " + self.teacher.last_name
