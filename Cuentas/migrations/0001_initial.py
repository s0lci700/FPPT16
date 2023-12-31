# Generated by Django 4.2.4 on 2023-09-06 15:34

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("A", "Alumno"),
                            ("P", "Profesor"),
                            ("NS", "No especificado"),
                        ],
                        default="NS",
                        help_text="Rol del usuario",
                        max_length=2,
                        verbose_name="Rol",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Correo electrónico del usuario",
                        max_length=254,
                        unique=True,
                        verbose_name="Correo electrónico",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        help_text="Nombre del usuario",
                        max_length=50,
                        verbose_name="Nombre",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        help_text="Apellido del usuario",
                        max_length=50,
                        verbose_name="Apellido",
                    ),
                ),
                (
                    "pronouns",
                    models.CharField(
                        blank=True,
                        help_text="Pronombres del usuario",
                        max_length=20,
                        verbose_name="Pronombres",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        default="perfiles/default.png",
                        upload_to="perfiles/avatars",
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(
                        blank=True,
                        help_text="Fecha de nacimiento del usuario",
                        null=True,
                        verbose_name="Fecha de nacimiento",
                    ),
                ),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(auto_now=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Usuario",
                "verbose_name_plural": "Usuarios",
                "ordering": ["last_name", "first_name", "role"],
            },
        ),
        migrations.CreateModel(
            name="TeacherProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        limit_choices_to={"role": "P"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teacherprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Perfil de profesor",
                "verbose_name_plural": "Perfiles de profesores",
            },
        ),
        migrations.CreateModel(
            name="StudentProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "year",
                    models.CharField(
                        choices=[("3", "Tercer Año"), ("4", "Cuarto Año")],
                        default="3",
                        max_length=1,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        limit_choices_to={"role": "A"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="studentprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Perfil de alumno",
                "verbose_name_plural": "Perfiles de alumnos",
            },
        ),
    ]
