from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import CustomUser


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
