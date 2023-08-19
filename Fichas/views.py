import logging
from logging import log

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from Cuentas.models import StudentProfile
from .forms import FichaForm
from .models import Ficha


# Create your views here.
def ficha_general_view(request):
    context = {
        "fichas": Ficha.objects.all(),
    }
    return render(request, "ficha.html", context)


@login_required
def ficha_create_view(request):
    if request.method == "POST":
        form = FichaForm(request.POST, request.FILES)
        if form.is_valid():
            ficha = form.save(commit=False)
            # Retrieve the StudentProfile corresponding to the logged-in user
            student_profile = StudentProfile.objects.get(user=request.user)
            
            # Assign the StudentProfile to the Ficha object
            ficha.student = student_profile
            ficha.save()
            return HttpResponseRedirect(reverse("ficha_detail", args=[ficha.id]))
        else:
            logging.log(msg="User: " + str(request.user) + str(form.errors), level=logging.INFO)
    else:
        form = FichaForm(user=request.user)

    return render(request, "ficha_create.html", {"form": form})


def ficha_detail_view(request, id):
    ficha = get_object_or_404(Ficha, id=id)
    return render(request, "ficha_detail.html", {"ficha": ficha})


def ficha_update_view(request, id):
    ficha = get_object_or_404(Ficha, id=id)
    if request.method == "POST":
        form = FichaForm(request.POST, request.FILES, instance=ficha)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ficha_detail", args=[ficha.id]))
    else:
        form = FichaForm(instance=ficha)

    return render(request, "ficha.html", {"form": form})


def ficha_delete_view(request, id):
    ficha = get_object_or_404(Ficha, id=id)
    if request.method == "POST":
        ficha.delete()
        return HttpResponseRedirect(reverse("ficha_general"))

    return render(request, "ficha_delete_confirm.html", {"ficha": ficha})
