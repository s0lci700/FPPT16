# Generated by Django 4.2.4 on 2023-08-04 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('main_image', models.ImageField(upload_to='images/')),
                ('complementary_images', models.ImageField(blank=True, upload_to='images/')),
                ('description', models.TextField()),
                ('analysis', models.TextField()),
                ('references', models.TextField()),
                ('keywords', models.TextField()),
                ('misc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ficha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Fichas.ficha')),
            ],
        ),
    ]
