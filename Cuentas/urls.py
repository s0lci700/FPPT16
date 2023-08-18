from django.urls import path
from .views import CustomUserRegister, CustomLoginView
from . import views
from . import forms
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # login, logout, register
    path('signup/', CustomUserRegister.as_view(), name='signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.home_view, name='home'),
    path('', views.landing_view, name='landing'),

    # list_views
    path('alumni/', views.alumni_list_view, name='alumni'),
    path('profesores/', views.profesor_list_view, name='profesores'),
    path('all_users/', views.all_users_list_view, name='all_users'),

]
