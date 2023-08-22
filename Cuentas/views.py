from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate
from django.views.generic import DetailView, ListView

from Fichas.models import Ficha
from .forms import CustomUserForm, LoginForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth import login

User = get_user_model()


# AUTH VIEWS
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, "You are now logged in.")
                    return redirect("landing")
                else:
                    messages.error(request, "Invalid email or password.")
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid email or password.")

    context = {"form": form}
    return render(request, "login.html", context)


# CRUD views
class RegisterView(CreateView):
    form_class = CustomUserForm
    model = CustomUser
    template_name = "register_view.html"

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = self.object.role
        if role == "A":
            student_profile = (
                self.object.studentprofile
            )  # Access the StudentProfile object
            context[
                "year"
            ] = (
                student_profile.year
            )  # Access the year attribute from the StudentProfile object
        elif role == "P":
            teacher_profile = self.object.teacherprofile
        return context


class EditUser(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = "edit_user.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"pk": self.object.pk})


class DeleteUser(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = CustomUser
    success_url = reverse_lazy("landing")
    template_name = "user_confirm_delete.html"

    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, "User deleted.")
        return super().delete(request, *args, **kwargs)


# class UploadFichaView(FormView):
#     form_class = FichaForm
#     template_name = "upload_ficha.html"
#
#     def form_valid(self, form):
#         return super().form_valid(form)


# General views


def landing_view(request):
    return render(request, "landing.html")


@login_required
def home_view(request):
    return render(request, "home.html")


# General List View with logic for different roles
class UserListView(ListView):
    context_object_name = "users"
    context = {
        "alumni": CustomUser.objects.filter(role="A"),
        "profesores": CustomUser.objects.filter(role="P"),
        "otros": CustomUser.objects.filter(role="NS"),
    }

    def get_template_names(self):
        role = self.kwargs.get("role")
        return f"{role}.html"

    def get_queryset(self):
        role = self.kwargs.get("role")

        if role == "all_users":
            return CustomUser.objects.all()

        role_mapping = {
            "alumni": "A",
            "profesores": "P",
        }

        return CustomUser.objects.filter(role=role_mapping[role])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs["role"] not in ["alumni", "profesores"]:
            users = context["users"]
            context["alumni"] = [user for user in users if user.role == "A"]
            context["profesores"] = [user for user in users if user.role == "P"]
            context["otros"] = [user for user in users if user.role not in ["A", "P"]]

        return context


# Detail views


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_profile = self.object.studentprofile  # Access the StudentProfile object
        user_fichas = Ficha.objects.filter(
            student=student_profile
        )  # Filter by StudentProfile object
        context["user_fichas"] = user_fichas
        context["role_display"] = self.object.get_role_display()

        return context
