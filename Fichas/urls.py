from django.urls import path
from .views import (
    ficha_general_view,
    ficha_create_view,
    ficha_detail_view,
    ficha_update_view,
    ficha_delete_view,
)

urlpatterns = [
    # These urls match the view functions and correctly pass an 'id' argument
    path('<int:id>/detail/', ficha_detail_view, name='ficha_detail'),
    path('<int:id>/update/', ficha_update_view, name='ficha_update'),
    path('<int:id>/delete/', ficha_delete_view, name='ficha_delete'),

    # These urls don't require an id so they can just call the function directly
    path('general/', ficha_general_view, name='ficha_general'),
    path('create/', ficha_create_view, name='ficha_create'),
]