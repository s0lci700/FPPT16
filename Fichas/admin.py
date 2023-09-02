from django.contrib import admin

from .models import Ficha, Review, Assignment

# Register your models here.

admin.site.site_header = "Administración de las Fichas"
admin.site.register(Ficha)
admin.site.register(Review)
admin.site.register(Assignment)
