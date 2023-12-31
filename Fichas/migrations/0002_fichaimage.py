# Generated by Django 4.2.4 on 2023-09-10 00:42

import Fichas.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Cuentas", "0001_initial"),
        ("Fichas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FichaImage",
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
                ("image", models.ImageField(upload_to=Fichas.models.upload_to)),
                (
                    "attributes",
                    models.CharField(
                        choices=[
                            ("MAIN", "main"),
                            ("FOTO", "fotograma"),
                            ("COMP", "complementaria"),
                            ("REF", "referencia"),
                            ("O", "otra"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "ficha",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="Fichas.ficha",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Cuentas.studentprofile",
                    ),
                ),
            ],
        ),
    ]
