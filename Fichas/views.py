import locale
from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db.models import Q, Case, When, BooleanField
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView

from Cuentas.models import StudentProfile
from .forms import FichaForm, AssignmentForm, FichaImageForm
from .models import Ficha, Assignment, FichaImage

FichaImageFormSet = modelformset_factory(
    FichaImage, form=FichaImageForm, extra=1, can_delete=True
)
User = get_user_model()


def get_assignments_and_open_assignments(user):
    current_datetime = timezone.now()
    assignments = Assignment.objects.annotate(
        ficha_filled=Case(
            When(fichas__student__user=user, then=True),
            default=False,
            output_field=BooleanField(),
        )
    )
    open_assignments = assignments.filter(
        Q(
            time_window_start__lte=current_datetime,
            time_window_end__gte=current_datetime,
        )
        | Q(fichas__status="Publicado")
    )
    return assignments, open_assignments


def handle_form_errors(form, formset):
    print("Form is not valid")
    for error in form.errors:
        print(error)
    for error in formset.errors:
        print(error)


def get_chilean_datetime():
    chile = pytz.timezone("America/Santiago")
    return datetime.now(chile)


def get_assignments_for_user(user):
    return get_assignments_and_open_assignments(user)


class BaseFichaView:
    model = Ficha
    form_class = FichaForm

    def get_object(self, queryset=None):
        return get_object_or_404(
            Ficha,
            student__user__id=self.kwargs["user_id"],
            assignment__id=self.kwargs["assignment_id"],
        )


class FichaCreateView(BaseFichaView, CreateView):
    template_name = "ficha_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment_id = self.kwargs.get("assignment_id")
        user_id = self.request.user.id
        context["assignment_id"] = assignment_id
        context["user_id"] = user_id

        # Initialize an empty queryset
        queryset = FichaImage.objects.none()

        try:
            ficha_id = get_object_or_404(
                Ficha, student__user__id=user_id, assignment__id=assignment_id
            ).id
            queryset = FichaImage.objects.filter(
                user=user_id, ficha=ficha_id, assignment=assignment_id
            )
        except Http404:
            # Ficha doesn't exist yet, so the queryset remains empty
            pass

        if self.request.POST:
            context["fichaimageformset"] = FichaImageFormSet(
                self.request.POST,
                self.request.FILES,
                prefix="fichaimage",
                queryset=queryset,
            )
        else:
            context["fichaimageformset"] = FichaImageFormSet(
                prefix="fichaimage",
                queryset=queryset,
            )

        return context

    def post(self, request, *args, **kwargs):
        assignment_id = self.kwargs.get("assignment_id")
        user_id = self.request.user.id

        form = self.get_form()
        formset = FichaImageFormSet(
            request.POST,
            request.FILES,
            queryset=FichaImage.objects.none(),  # Empty queryset for new Ficha
        )
        print(form)
        print(formset)
        if form.is_valid() and formset.is_valid():
            ficha = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    image = inline_form.cleaned_data["image"]
                    attributes = inline_form.cleaned_data["attributes"]
                    FichaImage.objects.create(
                        ficha=ficha, image=image, attributes=attributes
                    )
            return redirect("Fichas:ficha-list")
        else:
            handle_form_errors(form, formset)
            form = FichaForm()
            formset = FichaImageFormSet(queryset=FichaImage.objects.none())

            print("Form is not valid")
            for error in form.errors:
                print(error)
            for error in formset.errors:
                print(error)

        return render(
            request,
            "ficha_create.html",
            {
                "form": form,
                "formset": formset,
                "assignment_id": assignment_id,
                "user_id": user_id,
            },
        )

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        formset = FichaImageFormSet(queryset=FichaImage.objects.none())
        assignment_id = self.kwargs.get("assignment_id")
        assignment = get_object_or_404(Assignment, id=assignment_id)

        current_datetime = timezone.now()
        if (
            assignment.time_window_start > current_datetime
            or assignment.time_window_end < current_datetime
        ):
            raise Http404("La ficha no se puede crear en este momento")
        print(form)
        print(formset)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        print("Attempting to save Ficha with:")
        print("StudentID:", self.request.user.id)
        print("AssignmentID:", self.kwargs.get("assignment_id"))


class FichaUpdateView(BaseFichaView, UpdateView):
    template_name = "ficha_update.html"

    def form_valid(self, form):
        if not form.cleaned_data["main_image"]:
            form.instance.main_image = self.get_object().main_image
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("Fichas:ficha-list")


class FichaDeleteView(BaseFichaView, DeleteView):
    def post(self, request, *args, **kwargs):
        if "confirm_delete" in request.POST:
            return self.delete(request, *args, **kwargs)
        else:
            print("No se borro")
            pass

    def get_success_url(self):
        return reverse_lazy("ficha-list")


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


def ficha_detail_view(request, user_id, assignment_id):
    ficha = get_object_or_404(
        Ficha, student__user__id=user_id, assignment__id=assignment_id
    )
    fichaimages = FichaImage.objects.filter(ficha=ficha)
    print(user_id, assignment_id)
    return render(
        request,
        "ficha_detail.html",
        {
            "ficha": ficha,
            "user_id": user_id,
            "assignment_id": assignment_id,
            "fichaimages": fichaimages,
        },
    )


# class FichaCreateView(LoginRequiredMixin, CreateView):
#     model = Ficha
#     template_name = "ficha_create.html"
#     form_class = FichaForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["assignment_id"] = self.kwargs.get("assignment_id")
#         if self.request.POST:
#             context["images"] = FichaImageFormSet(
#                 self.request.POST, self.request.FILES, prefix="fichaimage"
#             )
#         else:
#             context["images"] = FichaImageFormSet(prefix="fichaimage")
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         formset = FichaImageFormSet(
#             request.POST, request.FILES, queryset=FichaImage.objects.none()
#         )
#         if form.is_valid() and formset.is_valid():
#             ficha = form.save()
#             for inline_form in formset:
#                 if inline_form.cleaned_data:
#                     image = inline_form.cleaned_data["image"]
#                     attributes = inline_form.cleaned_data["attributes"]
#                     FichaImage.objects.create(
#                         ficha=ficha, image=image, attributes=attributes
#                     )
#             return redirect("Fichas:ficha-list")
#         else:
#             form = FichaForm()
#             formset = FichaImageFormSet(queryset=FichaImage.objects.none())
#
#             print("Form is not valid")
#             for error in form.errors:
#                 print(error)
#             for error in formset.errors:
#                 print(error)
#
#         return render(
#             request,
#             "ficha_create.html",
#             {
#                 "form": form,
#                 "formset": formset,
#             },
#         )
#
#     def get(self, request, *args, **kwargs):
#         form = self.get_form()
#         formset = FichaImageFormSet(queryset=FichaImage.objects.none())
#         assignment_id = self.kwargs.get("assignment_id")
#         assignment = get_object_or_404(Assignment, id=assignment_id)
#
#         current_datetime = timezone.now()
#         if (
#             assignment.time_window_start > current_datetime
#             or assignment.time_window_end < current_datetime
#         ):
#             raise Http404("La ficha no se puede crear en este momento")
#         return super().get(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         images = context["images"]
#         print("Attempting to save Ficha with:")
#         print("StudentID:", self.request.user.id)
#         print("AssignmentID:", self.kwargs.get("assignment_id"))
#         # Existing code
#         if images.is_valid():
#             self.object = form.save()
#             images.instance = self.object
#             images.save()
#         student = self.request.user
#         student_profile = StudentProfile.objects.get(user=student)
#         assignment_id = self.kwargs.get("assignment_id")
#         assignment = get_object_or_404(Assignment, id=assignment_id)
#
#         # Check if a Ficha with the same student and assignment already exists
#         existing_ficha = Ficha.objects.filter(
#             student=student_profile, assignment=assignment
#         ).first()
#
#         if existing_ficha:
#             # If it exists, you can either update it, ignore it, or handle as per your requirement.
#             # For now, I'm throwing a ValidationError. You can customize this part.
#             raise ValidationError(
#                 "A Ficha with this student and assignment already exists."
#             )
#         else:
#             # If it doesn't exist, create a new Ficha
#             ficha = form.save(commit=False)
#             if "save_draft" in self.request.POST:
#                 ficha.status = "Borrador"
#             else:
#                 ficha.status = "Publicado"
#
#             ficha.student = student_profile
#             ficha.assignment = assignment
#
#             # Save the new Ficha
#             ficha.save()
#
#             formset = FichaImageFormSet(
#                 self.request.POST, self.request.FILES, instance=ficha
#             )
#             if formset.is_valid():
#                 formset.save()
#             else:
#                 print(formset.errors)
#
#             return super(FichaCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy("Fichas:ficha-list")


# class FichaUpdateView(LoginRequiredMixin, UpdateView):
#     model = Ficha
#     template_name = "ficha_update.html"
#     form_class = FichaForm
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(
#             Ficha,
#             student__user__id=self.kwargs["user_id"],
#             assignment__id=self.kwargs["assignment_id"],
#         )
#
#     def form_valid(self, form):
#         if not form.cleaned_data["main_image"]:
#             form.instance.main_image = self.get_object().main_image
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy("Fichas:ficha-list")
#
#
# class FichaDeleteView(LoginRequiredMixin, DeleteView):
#     model = Ficha
#     template_name = "ficha_delete_confirm.html"
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(
#             Ficha,
#             student__user__id=self.kwargs["user_id"],
#             assignment__id=self.kwargs["assignment_id"],
#         )
#
#     def post(self, request, *args, **kwargs):
#         if "confirm_delete" in request.POST:
#             return self.delete(request, *args, **kwargs)
#         else:
#             print("No se borro")
#             pass
#
#     def get_success_url(self):
#         return reverse_lazy("ficha-list")


def assignment_index(request):
    chile_time = get_chilean_datetime()

    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Set locale to Spanish
    weekday = chile_time.strftime("%A")  # Gives day of the week
    day_number = chile_time.day  # Gives the day number
    month = chile_time.strftime("%B")  # Gives the month
    year = chile_time.year  # Gives the year

    context = {
        "weekday": weekday,
        "day_number": day_number,
        "month": month,
        "year": year,
        # ... your other context data
    }
    return render(request, "assignment_index.html", context)


def assignment_list(request):
    assignments, open_assignments = get_assignments_for_user(request.user)
    form = AssignmentForm()
    context = {
        "assignments": assignments,  # This now includes both open and closed assignments
        "open_assignments": open_assignments,  # This is just open assignments
        "form": form,
    }
    return render(
        request,
        "components/assignment-list.html",
        context,
    )


# In Fichas.views.py
def create_assignment(request):
    assignments = Assignment.objects.annotate(
        ficha_filled=Case(
            When(fichas__student__user=request.user, then=True),
            default=False,
            output_field=BooleanField(),
        )
    )
    # You can still get open_assignments if needed
    current_datetime = timezone.now()
    open_assignments = assignments.filter(
        Q(
            time_window_start__lte=current_datetime,
            time_window_end__gte=current_datetime,
        )
        | Q(fichas__status="Publicado")
    )
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            new_assignment = form.save()
            context = {
                "assignment": new_assignment,
                "assignments": assignments,
                "open_assignments": open_assignments,
            }
            if request.htmx:
                return render(
                    request,
                    "components/assignment-list.html",
                    context,
                )
    else:
        # This is for GET or any other method
        form = AssignmentForm()
        context = {
            "form": form,
            "assignments": assignments,
            "open_assignments": open_assignments,
        }
        if request.htmx:
            return render(request, "components/create-assignment-form.html", context)
        else:
            return render(request, "assignment_index.html", context)


def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == "POST":
        print("POST")
        form = AssignmentForm(request.POST, instance=assignment)
        if request.htmx:
            print("HTMX")
            if form.is_valid():
                form.save()
                return redirect("Fichas:assignment-list")
        else:
            print("No htmx")
            if form.is_valid():
                form.save()
                return redirect("Fichas:assignment-list")
    else:
        print("GET")
        form = AssignmentForm(instance=assignment)
        if request.htmx:
            print("HTMX")
            return render(
                request,
                "components/update-assignment-form.html",
                {"form": form, "assignment": assignment},
            )
        else:
            print("No htmx")
            return render(
                request,
                "assignment_update.html",
                {
                    "form": form,
                    "assignment": assignment,
                },
            )


def assignment_delete_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == "POST":
        if "confirm_delete" in request.POST:
            assignment.delete()
            return redirect("Fichas:assignment-list")
        else:
            return redirect("Fichas:assignment-list")
    else:
        context = {
            "assignment": assignment,
        }
        return render(request, "assignment_delete_confirm.html", context)
