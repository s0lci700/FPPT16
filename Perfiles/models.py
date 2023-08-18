from django.db import models
from Cuentas.models import CustomUser


# Create your models here.
class Perfil(models.Model):
    # perfil de usuario tipo alumno previamente definido en el modelo User
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="media/perfiles/profile_pictures",
        default="media/perfiles/profile_pictures",
        blank=True,
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
