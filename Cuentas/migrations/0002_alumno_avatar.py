# Generated by Django 4.2.4 on 2023-08-15 00:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Cuentas", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="alumno",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="Perfiles/static/default.png",
                upload_to="static/avatars",
            ),
        ),
    ]
