from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate
from django.views.generic import DetailView, ListView

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
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect("landing")
            else:
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
            context['year'] = self.object.year
        elif role == "P":
            pass
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

    def get_template_names(self):
        role = self.kwargs.get("role")
        return f"{role}.html"

    def get_queryset(self):
        role = self.kwargs.get("role")
        role_mapping = {
            'alumni': 'A',
            'profesores': 'P',
            'all_users': CustomUser.objects.all(),
        }
        return CustomUser.objects.filter(role=role_mapping[role])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs['role'] == 'all_users':
            users = context['users']
            context['alumni'] = [user for user in users if user.role == "A"]
            context['profesores'] = [user for user in users if user.role == "P"]
            context['otros'] = [user for user in users if user.role not in ["A", "P"]]

        return context


# @login_required
# def alumni_list_view(request):
#     context = {
#         "alumni": CustomUser.objects.filter(role="A"),
#     }
#     return render(request, "alumni.html", context)

# class AlumniListView(ListView):
#     model = CustomUser
#     template_name = "alumni.html"
#     context_object_name = "alumni"
#     queryset = CustomUser.objects.filter(role="A")

# @login_required
# def profesor_list_view(request):
#     context = {
#         "profesores": CustomUser.objects.filter(role="P"),
#     }
#     return render(request, "profesores.html", context)

# class ProfesorListView(ListView):
#     model = CustomUser
#     template_name = "profesores.html"
#     context_object_name = "profesores"
#     queryset = CustomUser.objects.filter(role="P")

# @login_required
# def all_users_list_view(request):
#     users = CustomUser.objects.all()
#     students = [user for user in users if user.role == "A"]
#     teachers = [user for user in users if user.role == "P"]
#     others = [user for user in users if user.role not in ["A", "P"]]
#
#     context = {
#         "users": users,
#         "alumni": students,
#         "profesores": teachers,
#         "otros": others,
#     }
#     return render(request, "all_users.html", context)


# Detail views

class UserDetailView(DetailView):
    model = CustomUser

    def get_template_names(self):
        role = self.object.role
        if role == "A":
            return "alumni_detail.html"
        elif role == "P":
            return "profesor_detail.html"
        elif role == "NS":
            raise ValueError("User has no role, only users with a role can be displayed.")
        else:
            return "user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = self.object.role
        context['role'] = role
        if role == "A":
            context['year'] = self.object.year
        elif role == "P":
            pass
        return context

