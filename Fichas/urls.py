from django.urls import path
from .views import FichaCreateUpdateDeleteView, ficha_general_view

urlpatterns = [
    path('fichas/', ficha_general_view, name='ficha-list'),
    path('fichas/create/', FichaCreateUpdateDeleteView.as_view(), name='ficha-create'),
    path('fichas/<int:pk>/', FichaCreateUpdateDeleteView.as_view(), name='ficha-detail'),
    path('fichas/<int:pk>/update/', FichaCreateUpdateDeleteView.as_view(), name='ficha-update'),
    path('fichas/<int:pk>/delete/', FichaCreateUpdateDeleteView.as_view(), name='ficha-delete'),
]


