# Generated by Django 4.2.4 on 2023-08-15 00:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Perfiles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="perfil",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="Perfiles/static/default.png",
                upload_to="static/avatars",
            ),
        ),
    ]
