# Generated by Django 4.2.4 on 2023-08-04 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Fichas', '0001_initial'),
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.profesor'),
        ),
        migrations.AddField(
            model_name='ficha',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.alumno'),
        ),
    ]
