from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Alumno, Profesor
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    exclude = ("username", 'last_login', 'date_joined')
    USERNAME_FIELD = "email"
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "first_name", "last_name", 'avatar')
    fieldsets = (
        (None, {"fields": ("email", "password", 'avatar')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_student', 'is_teacher', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ()}),
    )

    list_filter = ("is_student", "is_teacher", "is_staff", "is_superuser")
    ordering = ("last_name", "first_name")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Alumno)
admin.site.register(Profesor)
