from django.urls import path
from .views import (
    FichaCreateView,
    FichaUpdateView,
    FichaDeleteView,
    ficha_general_view,
    ficha_detail_view,
    assignment_list,
    create_assignment,
)

urlpatterns = [
    path("", ficha_general_view, name="ficha-list"),
    path("create/<int:assignment_id>/", FichaCreateView.as_view(), name="ficha-create"),
    path("<int:id>/", ficha_detail_view, name="ficha-detail"),
    path("<int:id>/update/", FichaUpdateView.as_view(), name="ficha-update"),
    path("<int:id>/delete/", FichaDeleteView.as_view(), name="ficha-delete"),
    # path("<int:id>/delete-confirm/", ficha_delete_confirm, name="ficha-delete-confirm"),
    path("assignment/", assignment_list, name="assignment-list"),
    path("assignment/create/", create_assignment, name="assignment-create"),
]
