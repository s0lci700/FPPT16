# Signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from Cuentas.models import CustomUser, StudentProfile, TeacherProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'A':
            StudentProfile.objects.create(user=instance)
        elif instance.role == 'P':
            TeacherProfile.objects.create(user=instance)