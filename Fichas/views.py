from datetime import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from Cuentas.models import StudentProfile
from .forms import FichaForm, AssignmentForm
from .models import Ficha, Assignment

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assignment_id"] = self.kwargs.get("assignment_id")
        return context

    def get(self, request, *args, **kwargs):
        assignment_id = self.kwargs.get("assignment_id")
        assignment = get_object_or_404(Assignment, id=assignment_id)

        current_datetime = timezone.now()
        if (
            assignment.time_window_start > current_datetime
            or assignment.time_window_end < current_datetime
        ):
            raise Http404("La ficha no se puede crear en este momento")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ficha = form.save(commit=False)
        if "save_draft" in self.request.POST:
            ficha.status = "Borrador"
        else:
            ficha.status = "Publicado"
        student = self.request.user
        student_profile = StudentProfile.objects.get(user=student)
        ficha.student = student_profile

        assignment_id = self.kwargs.get("assignment_id")
        assignment = get_object_or_404(Assignment, id=assignment_id)
        ficha.assignment = assignment

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


def assignment_list(request):
    assignments = Assignment.objects.all()
    current_datetime = timezone.now()
    open_assignments = Assignment.objects.filter(
        Q(
            time_window_start__lte=current_datetime,
            time_window_end__gte=current_datetime,
        )
        | Q(fichas__status="Publicado")
    )
    form = AssignmentForm()
    context = {
        "assignments": assignments,
        "open_assignments": open_assignments,
        "form": form,
    }
    return render(
        request,
        "assignment_list.html",
        context,
    )


def create_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("assignment-list")
    else:
        form = AssignmentForm()
    return render(request, "components/ACreateModal.html", {"form": form})
