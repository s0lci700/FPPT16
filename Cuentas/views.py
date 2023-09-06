from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, resolve
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from taggit.models import Tag

from Fichas.models import Ficha, Assignment
from .forms import CustomUserForm, LoginForm
from .models import CustomUser

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(pk=self.object.pk)
        context["user"] = user
        return context

    def get_success_url(self):
        return reverse_lazy("Cuentas:user_detail", kwargs={"pk": self.object.pk})

    def get_initial(self):
        initial = super().get_initial()
        initial["email"] = self.object.email
        initial["role"] = self.object.role
        initial["birth_date"] = self.object.birth_date
        # initial["year"] = self.object.year
        return initial

    def form_valid(self, form):
        print("Form is valid")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is not valid", form.errors)
        return super().form_invalid(form)


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
    assignments = Assignment.objects.all()

    current_datetime = timezone.now()
    context = {
        "current_datetime": current_datetime,
        "assignments": assignments,
    }
    return render(request, "home.html", context)


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
def user_detail_redirect(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if user.role == "A":
        return redirect("Cuentas:student_detail", pk=pk)
    elif user.role == "P":
        return redirect("Cuentas:teacher_detail", pk=pk)


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        # Determine the role based on the URL name
        url_name = resolve(self.request.path_info).url_name
        if url_name == "student_detail":
            return get_object_or_404(CustomUser, pk=pk, role="A")
        elif url_name == "teacher_detail":
            return get_object_or_404(CustomUser, pk=pk, role="P")
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.role == "A":
            student_profile = self.object.studentprofile
            user_fichas = student_profile.user_ficha.all()
            tags = Tag.objects.filter(ficha__in=user_fichas).distinct()
            context["tags"] = tags
            context["user_fichas"] = user_fichas
            student = CustomUser.objects.get(pk=self.object.pk)
            context["student"] = student
        elif self.object.role == "P":
            teacher_profile = self.object.teacherprofile
        return context


class MyFichasViews(ListView, LoginRequiredMixin):
    model = Ficha
    template_name = "ficha_list.html"
    context_object_name = "fichas"

    def get_queryset(self):
        active_user = self.request.user.pk
        user = CustomUser.objects.get(pk=active_user)
        if user.role == "A":
            student_profile = user.studentprofile
            return Ficha.objects.filter(student=student_profile).all()
        else:
            raise Http404
