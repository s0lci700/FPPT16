
from django.urls import path
from . import views
urlpatterns = [
    path('alumni/', views.alumni_list_view, name='alumni'),
    path('profesores/', views.profesor_list_view, name='profesores'),
    path('all_users/', views.all_users_list_view, name='all_users'),
]