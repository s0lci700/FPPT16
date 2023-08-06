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
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from Home.views import home_view
from Usuarios.views import CustomUserRegister
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home_view, name='home'),
    path('register/', CustomUserRegister.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='login.html',
        next_page='home',
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include('Usuarios.urls')),
    path('fichas/', include('Fichas.urls')),
    path('perfiles/', include('Perfiles.urls')) ,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
