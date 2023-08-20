import logging
from logging import log

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
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
    return render(request, "ficha.html", context)


def ficha_detail_view(request, id):
    ficha = get_object_or_404(Ficha, id=id)
    return render(request, "ficha_detail.html", {"ficha": ficha})


class FichaCreateView(LoginRequiredMixin, CreateView):
    model = Ficha
    template_name = "ficha_create.html"
    form_class = FichaForm

    def form_valid(self, form):
        ficha = form.save(commit=False)
        ficha.status = "Borrador" if "save_draft" in self.request.POST else "Publicado"
        student = self.request.user
        student_profile = StudentProfile.objects.get(user=student)
        ficha.student = student_profile
        ficha.save()
        return render(self.request, "ficha_partial.html", {"ficha": ficha})

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class FichaUpdateView(LoginRequiredMixin, UpdateView):
    model = Ficha
    template_name = "ficha_update.html"
    form_class = FichaForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {"msg": "Update successful!"}
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class FichaDeleteView(LoginRequiredMixin, DeleteView):
    model = Ficha
    template_name = "ficha_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {"msg": "Ficha deleted!"}
        return JsonResponse(data)


# @login_required
# class FichaCreateUpdateDeleteView(
#     LoginRequiredMixin, CreateView, UpdateView, DeleteView
# ):
#     model = Ficha
#     template_name = "ficha_create.html"
#     form_class = FichaForm
#
#     def get_object(self, queryset=None):
#         if self.kwargs.get("pk"):
#             return super().get_object(queryset)
#         return None
#
#     def post(self, request, *args, **kwargs):
#         if "delete" in request.POST:
#             return render(
#                 request, "ficha_delete_confirm.html", {"ficha": self.get_object()}
#             )
#         elif "confirm_delete" in request.POST:
#             # Check password confirmation here
#             if request.user.check_password(request.POST["password"]):
#                 return self.delete(request, *args, **kwargs)
#             else:
#                 return render(
#                     request,
#                     "ficha_delete_confirm.html",
#                     {"ficha": self.get_object(), "error": "Incorrect password"},
#                 )
#         return super().post(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         ficha = form.save(commit=False)
#         if "save_draft" in self.request.POST:
#             ficha.status = "Borrador"
#         else:
#             ficha.status = "Publicado"
#         student = self.request.user
#         student_profile = StudentProfile.objects.get(user=student)
#         ficha.student = student_profile
#         ficha.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy(
#             "ficha_general"
#         )  # Redirect to the list of fichas after successful action


# @login_required
# def ficha_create_view(request):
#     if request.method == "POST":
#         form = FichaForm(request.POST, request.FILES)
#         if form.is_valid():
#             ficha = form.save(commit=False)
#             # Retrieve the StudentProfile corresponding to the logged-in user
#             student_profile = StudentProfile.objects.get(user=request.user)
#
#             # Assign the StudentProfile to the Ficha object
#             ficha.student = student_profile
#             ficha.save()
#             return HttpResponseRedirect(reverse("ficha_detail", args=[ficha.id]))
#         else:
#             logging.log(msg="User: " + str(request.user) + str(form.errors), level=logging.INFO)
#     else:
#         form = FichaForm(user=request.user)
#
#     return render(request, "ficha_create.html", {"form": form})
# def ficha_delete_view(request, id):
#     ficha = get_object_or_404(Ficha, id=id)
#     if request.method == "POST":
#         ficha.delete()
#         return HttpResponseRedirect(reverse("ficha_general"))
#
#     return render(request, "ficha_delete_confirm.html", {"ficha": ficha})
# def ficha_update_view(request, id):
#     ficha = get_object_or_404(Ficha, id=id)
#     if request.method == "POST":
#         form = FichaForm(request.POST, request.FILES, instance=ficha)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("ficha_detail", args=[ficha.id]))
#     else:
#         form = FichaForm(instance=ficha)
#
#     return render(request, "ficha.html", {"form": form})
