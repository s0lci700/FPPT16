from django.urls import path
from . import views
urlpatterns = [
    path('', views.ficha_general_view, name='ficha_general'),
    path('create/', views.ficha_create_view, name='ficha_create'),
    path('<int:id>/', views.ficha_detail_view, name='ficha_detail'),
    path('<int:id>/update/', views.ficha_update_view, name='ficha_update'),
    path('<int:id>/delete/', views.ficha_delete_view, name='ficha_delete'),
]
