from django.contrib import admin

from .models import CustomUser, Alumno, Profesor

# Register your models here.
admin.site.site_header = "Administración de la plataforma"
admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(CustomUser)
