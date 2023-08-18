from django.contrib import messages
from django.shortcuts import render

from .forms import CustomUserCreationForm
from .forms import CustomAuthForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login


class CustomLoginView(FormView):
    template_name = "login.html"
    form_class = CustomAuthForm
    success_url = reverse_lazy("landing")

    def form_valid(self, form):
        user = form.get_user()
        print("User from form:", user)  # Debugging line
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "You are now logged in.")
        else:
            messages.error(self.request, "Invalid email or password.")
        return super().form_valid(form)

    def form_invalid(self, form):
        message = "Invalid email or password."
        return self.render_to_response(
            self.get_context_data(form=form, error_message=message)
        )


# Create your views here.


def landing_view(request):
    return render(request, "landing.html")


@login_required
def home_view(request):
    return render(request, "home.html")


# def login_view(request):
#     if request.method == "POST":
#         form = CustomAuthForm(data=request.POST)
#         if form.is_valid():
#             message = "You are now logged in."
#             login(request, form.get_user())
#             return render(request, "home.html", {"message": message})
#         else:
#             message = "Invalid email or password."
#             return render(request, "login.html", {"form": form, "message": message})
#     else:
#         form = CustomAuthForm()
#         return render(request, "login.html", {"form": form})


class CustomUserRegister(FormView):
    template_name = "register_view.html"
    form_class = CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


@login_required
def alumni_list_view(request):
    context = {
        "alumni": CustomUser.objects.filter(is_student=True),
    }
    return render(request, "alumni.html", context)


@login_required
def profesor_list_view(request):
    context = {
        "profesores": CustomUser.objects.filter(is_teacher=True),
    }
    return render(request, "profesores.html", context)


@login_required
def all_users_list_view(request):
    context = {
        "users": CustomUser.objects.all(),
    }
    return render(request, "all_users.html", context)
