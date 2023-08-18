from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from .forms import CustomUserCreationForm
from .forms import CustomAuthForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login


# Authentication views
class CustomLoginView(FormView):
    template_name = "login.html"
    form_class = CustomAuthForm
    success_url = reverse_lazy("landing")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, "You are now logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        message = "Invalid email or password."
        return self.render_to_response(
            self.get_context_data(form=form, error_message=message)
        )


class CustomUserRegister(FormView):
    template_name = "register_view.html"
    form_class = CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


# General views


def landing_view(request):
    return render(request, "landing.html")


@login_required
def home_view(request):
    return render(request, "home.html")


# List views


@login_required
def alumni_list_view(request):
    context = {
        "alumni": CustomUser.objects.filter(studentprofile__isnull=False),
    }
    return render(request, "alumni.html", context)


@login_required
def profesor_list_view(request):
    context = {
        "profesores": CustomUser.objects.filter(teacherprofile__isnull=False),
    }
    return render(request, "profesores.html", context)


@login_required
def all_users_list_view(request):
    users = CustomUser.objects.all()
    students = [user for user in users if user.is_student]
    teachers = [user for user in users if user.is_teacher]
    others = [user for user in users if not user.is_student and not user.is_teacher]

    context = {
        "users": users,
        "alumni": students,
        "profesores": teachers,
        "otros": others,
    }
    return render(request, "all_users.html", context)


# Detail views


def student_detail_view(request, pk):
    student = get_object_or_404(CustomUser, id=pk)
    assert student.role == "A", "This user is not a student."
    return render(request, "student_detail.html", {"user": student})


def teacher_detail_view(request, pk):
    teacher = get_object_or_404(CustomUser, id=pk)
    assert teacher.role == "P", "This user is not a teacher."
    return render(request, "teacher_detail.html", {"user": teacher})


def user_detail_view(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    if user.role == "A":
        return student_detail_view(request, pk)
    elif user.role == "P":
        return teacher_detail_view(request, pk)
    else:
        return render(request, "user_detail.html", {"user": user})
