# Generated by Django 4.2.4 on 2023-09-06 15:34

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Cuentas", "0001_initial"),
        ("taggit", "0005_auto_20220424_2025"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assignment",
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
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("time_window_start", models.DateTimeField()),
                ("time_window_end", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Ficha",
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
                    "status",
                    models.CharField(
                        choices=[("Borrador", "Borrador"), ("Publicado", "Publicado")],
                        default="Borrador",
                        max_length=10,
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                (
                    "main_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="fichas/images/"
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("analysis", models.TextField(blank=True)),
                ("references", models.TextField(blank=True)),
                ("misc", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fichas",
                        to="Fichas.assignment",
                    ),
                ),
                (
                    "keywords",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_ficha",
                        related_query_name="fichas",
                        to="Cuentas.studentprofile",
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "assignment")},
            },
        ),
        migrations.CreateModel(
            name="Keywords",
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
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                ("review", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "ficha",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Fichas.ficha"
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Cuentas.teacherprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ComplementaryImage",
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
                ("images", models.ImageField(upload_to="images/")),
                (
                    "ficha",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="complementary_images",
                        to="Fichas.ficha",
                    ),
                ),
            ],
        ),
    ]
