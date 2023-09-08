# Fichas.urls
from django.urls import path

from .views import (
    FichaCreateView,
    FichaUpdateView,
    FichaDeleteView,
    ficha_general_view,
    ficha_detail_view,
    assignment_list,
    create_assignment,
    assignment_update_view,
    assignment_delete_view,
)

urlpatterns = [
    path("", ficha_general_view, name="ficha-list"),
    path(
        "<int:user_id>/create/<int:assignment_id>/",
        FichaCreateView.as_view(),
        name="ficha-create",
    ),
    path("<int:user_id>/<int:assignment_id>/", ficha_detail_view, name="ficha-detail"),
    path(
        "<int:user_id>/<int:assignment_id>/update/",
        FichaUpdateView.as_view(),
        name="ficha-update",
    ),
    path(
        "<int:user_id>/<int:assignment_id>/delete/",
        FichaDeleteView.as_view(),
        name="ficha-delete",
    ),
    path("assignment/", assignment_list, name="assignment-list"),
    path("assignment/create/", create_assignment, name="assignment-create"),
    path(
        "assignment/<int:assignment_id>/update/",
        assignment_update_view,
        name="assignment-update",
    ),
    path(
        "assignment/<int:assignment_id>/delete/",
        assignment_delete_view,
        name="assignment-delete",
    ),
]
