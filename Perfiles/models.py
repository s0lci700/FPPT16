from django.db import models
from Cuentas.models import CustomUser


# Create your models here.
class Perfil(models.Model):
    # perfil de usuario tipo alumno previamente definido en el modelo User
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="media/perfiles/profile_pictures", default="media/perfiles/profile_pictures", blank=True
    )

    if CustomUser.is_student:

        def __str__(self):
            return self.user.first_name + " " + self.user.last_name

    elif CustomUser.is_teacher:

        def __str__(self):
            return "Prof. " + self.user.first_name + " " + self.user.last_name

    else:
        print("Usuario no definido")

    class Meta:
        verbose_name_plural = "Perfiles"
