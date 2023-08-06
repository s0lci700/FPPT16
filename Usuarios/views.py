from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import AlumnoForm, ProfesorForm, CustomUserForm
from .models import CustomUser


# Create your views here.

class CustomUserRegister(FormView):
    template_name = 'register_view.html'
    form_class = CustomUserForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


def alumni_list_view(request):
    context = {
        'alumni': CustomUser.objects.filter(is_student=True),
    }
    return render(request, 'alumni.html', context)


def profesor_list_view(request):
    context = {
        'profesores': CustomUser.objects.filter(is_teacher=True),
    }
    return render(request, 'profesores.html', context)

def all_users_list_view(request):
    context = {
        'users': CustomUser.objects.all(),
    }
    return render(request, 'all_users.html', context)