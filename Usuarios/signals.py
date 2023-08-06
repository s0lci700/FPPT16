from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from Perfiles.models import Perfil


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
