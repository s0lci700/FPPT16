from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from Cuentas.models import StudentProfile
from .forms import FichaForm
from .models import Ficha

User = get_user_model()


# Create your views here.
def ficha_general_view(request):
    if hasattr(request.user, "studentprofile"):
        student_profile = StudentProfile.objects.get(user=request.user)
        fichas = Ficha.objects.filter(
            Q(student=student_profile, status="Borrador") | Q(status="Publicado")
        )
    else:
        fichas = Ficha.objects.filter(status="Publicado")

    context = {
        "fichas": fichas,
    }
    return render(request, "ficha_list.html", context)


def ficha_detail_view(request, id):
    ficha = get_object_or_404(Ficha, id=id)
    return render(request, "ficha_detail.html", {"ficha": ficha})


class FichaCreateView(LoginRequiredMixin, CreateView):
    model = Ficha
    template_name = "ficha_create.html"
    form_class = FichaForm

    def form_valid(self, form):
        ficha = form.save(commit=False)
        if "save_draft" in self.request.POST:
            ficha.status = "Borrador"
        else:
            ficha.status = "Publicado"
        student = self.request.user
        student_profile = StudentProfile.objects.get(user=student)
        ficha.student = student_profile
        ficha.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ficha-list")


class FichaUpdateView(LoginRequiredMixin, UpdateView):
    model = Ficha
    template_name = "ficha_update.html"
    form_class = FichaForm

    def get_object(self, queryset=None):
        return get_object_or_404(Ficha, id=self.kwargs["id"])

    def form_valid(self, form):
        if not form.cleaned_data["main_image"]:
            form.instance.main_image = self.get_object().main_image
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ficha-list")


class FichaDeleteView(LoginRequiredMixin, DeleteView):
    model = Ficha
    template_name = "ficha_delete_confirm.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Ficha, id=self.kwargs["id"])

    def post(self, request, *args, **kwargs):
        if "confirm_delete" in request.POST:
            return self.delete(request, *args, **kwargs)
        else:
            print("No se borro")
            pass

    def get_success_url(self):
        return reverse_lazy("ficha-list")
