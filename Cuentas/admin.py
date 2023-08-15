from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Alumno, Profesor
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_student', 'is_teacher', 'is_staff', 'is_active',)


admin.site.site_header = "Administración de la plataforma"
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Alumno)
admin.site.register(Profesor)
