"""
URL configuration for FPPT16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Cuentas.general_views import home_view, landing_view, login_modal as lmodal

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include(("Cuentas.urls", "Cuentas"), namespace="cuentas")),
    path("fichas/", include(("Fichas.urls", "Fichas"), namespace="fichas")),
    path("__reload__/", include("django_browser_reload.urls")),
    # general views
    path("home/", home_view, name="home"),
    path("", landing_view, name="landing"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "FPPT16 Admin"
admin.site.site_title = "FPPT16 Admin Portal"
admin.site.index_title = "Welcome to FPPT16 Portal"
