from django.contrib.auth.views import LogoutView
from django.urls import path, include  # Note the inclusion of 'include'
from . import views
from .views import (
    UserListView,
    UserDetailView,
    user_detail_redirect,
    MyFichasViews,
)
from .auth_views import login_view
from .crud_views import RegisterView, EditUser, DeleteUser


urlpatterns = [
    # login, logout
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # CUD views
    path("signup/", RegisterView.as_view(), name="signup"),
    path("user/<int:pk>/edit/", EditUser.as_view(), name="edit_user"),
    path("user/<int:pk>/delete/", DeleteUser.as_view(), name="delete_user"),
    # R View/Detail User View
    path("user/student/<int:pk>/", UserDetailView.as_view(), name="student_detail"),
    path("user/teacher/<int:pk>/", UserDetailView.as_view(), name="teacher_detail"),
    path("user/<int:pk>/", user_detail_redirect, name="user_detail"),
    # list_views for each role
    path("alumni/", UserListView.as_view(), {"role": "alumni"}, name="alumni"),
    path(
        "profesores/", UserListView.as_view(), {"role": "profesores"}, name="profesores"
    ),
    path("all_users/", UserListView.as_view(), {"role": "all_users"}, name="all_users"),
    # listview for fichas by user
    path("user/<int:pk>/fichas/", MyFichasViews.as_view(), name="my-fichas"),
    # Nested Fichas URLs
    path(
        "user/<int:pk>/fichas/", include(("Fichas.urls", "Fichas"))
    ),  # This line will connect Cuentas and Fichas
    path("user/student/<int:pk>/dossier/", views.get_dossier, name="get_dossier"),
]
