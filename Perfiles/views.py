from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib import messages
from Cuentas.models import CustomUser


# Create your views here.
# @login_required
# def perfil(request):
#     if request.method == 'POST':
#         user_form = UpdateUserForm(request.POST, instance=request.user)
#         profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.perfil)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('perfil')
#     else:
#         user_form = UpdateUserForm(instance=request.customuser)
#         profile_form = UpdateProfileForm(instance=request.perfil.user)
#
#     return render(request, 'perfil.html', {'user_form': user_form, 'profile_form': profile_form})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UpdateUserForm, UpdateProfileForm


@login_required
def perfil(request):
    user_form = profile_form = None

    if request.method == 'POST':
        user_form, profile_form = get_post_forms(request)
        if validate_forms(user_form, profile_form):
            save_forms(user_form, profile_form)
            messages.success(request, f'Your account has been updated!')
            return redirect('perfil')
    else:
        user_form, profile_form = get_default_forms(request)

    return render(request, 'perfil.html', get_context(user_form, profile_form))


def get_post_forms(request):
    user_form = UpdateUserForm(request.POST, instance=request.user)
    profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.perfil)
    return user_form, profile_form


def get_default_forms(request):
    user_form = UpdateUserForm(instance=request.customuser)
    profile_form = UpdateProfileForm(instance=request.perfil.user)
    return user_form, profile_form


def get_context(user_form, profile_form):
    return {'user_form': user_form, 'profile_form': profile_form}


def validate_forms(user_form, profile_form):
    return user_form.is_valid() and profile_form.is_valid()


def save_forms(user_form, profile_form):
    user_form.save()
    profile_form.save()