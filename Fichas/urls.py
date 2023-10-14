# Fichas.urls
from django.urls import path

from .views import (
    FichaCreateView,
    FichaUpdateView,
    FichaDeleteView,
    ficha_general_view,
    ficha_detail_view,
    assignment_index,
    create_assignment,
    assignment_delete_view,
    assignment_list,
    edit_assignment,
    review_create_view,
    review_update_view,
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
    path("assignment/", assignment_index, name="assignment"),
    path("assignment/list/", assignment_list, name="assignment-list"),
    path("assignment/create/", create_assignment, name="assignment-create"),
    path(
        "assignment/<int:pk>/update/",
        edit_assignment,
        name="assignment-update",
    ),
    path(
        "assignment/<int:pk>/delete/",
        assignment_delete_view,
        name="assignment-delete",
    ),
    path(
        "<int:user_id>/<int:assignment_id>/review/",
        review_create_view,
        name="review-create",
    ),
    path(
        "<int:user_id>/<int:assignment_id>/review-update/",
        review_update_view,
        name="review-update",
    ),
]
