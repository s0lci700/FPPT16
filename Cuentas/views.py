from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import AlumnoForm, ProfesorForm, CustomUserForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_view(request):
    return render(request, 'home.html')


class CustomUserRegister(FormView):
    template_name = 'register_view.html'
    form_class = CustomUserForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


@login_required
def alumni_list_view(request):
    context = {
        'alumni': CustomUser.objects.filter(is_student=True),
    }
    return render(request, 'alumni.html', context)


@login_required
def profesor_list_view(request):
    context = {
        'profesores': CustomUser.objects.filter(is_teacher=True),
    }
    return render(request, 'profesores.html', context)


@login_required
def all_users_list_view(request):
    context = {
        'users': CustomUser.objects.all(),
    }
    return render(request, 'all_users.html', context)
