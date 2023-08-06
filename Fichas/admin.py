from django.contrib import admin

from .models import Ficha, Review

# Register your models here.

admin.site.site_header = "Administración de las forms"
admin.site.register(Ficha)
admin.site.register(Review)
