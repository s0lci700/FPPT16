from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# local views
from .models import Perfil
from . import views

urlpatterns = [
    path('', views.perfil, name='perfil'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
