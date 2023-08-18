from django.urls import path
from . import views
urlpatterns = [
    path('', views.ficha_general_view, name='ficha_general'),
    path('create/', views.ficha_create_view, name='ficha_create'),
    path('ficha/<int:id>/', views.ficha_detail_view, name='ficha_detail'),
    path('ficha/<int:id>/update/', views.ficha_update_view, name='ficha_update'),
    path('ficha/<int:id>/delete/', views.ficha_delete_view, name='ficha_delete'),
]
