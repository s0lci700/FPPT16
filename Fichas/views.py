import locale
from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q, Case, When, BooleanField
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from embed_video.backends import detect_backend, UnknownBackendException

from Cuentas.models import StudentProfile, TeacherProfile
from .forms import FichaForm, AssignmentForm, ReviewForm
from .models import Ficha, Assignment, Review

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
        return context

    def post(self, request, *args, **kwargs):
        assignment_id = self.kwargs.get("assignment_id")
        user_id = self.request.user.id

        form = self.get_form()
        print(form)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.student_id = user_id
            ficha.assignment_id = assignment_id
            button_clicked = request.POST.get("submit")
            print(button_clicked)

            if button_clicked == "publish":
                # Publish the Ficha
                ficha.status = "Publicado"
            elif button_clicked == "draft":
                # Save as a draft
                ficha.status = "Borrador"
            ficha.save()
            return redirect(
                "Fichas:ficha-list",
            )  # changed here
        else:
            handle_form_errors(form)
            form = FichaForm()

            print("Form is not valid")
            for error in form.errors:
                print(error)

        return render(
            request,
            "ficha_create.html",
            {
                "form": form,
                "assignment_id": assignment_id,
                "user_id": user_id,
            },
        )

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        assignment_id = self.kwargs.get("assignment_id")
        assignment = get_object_or_404(Assignment, id=assignment_id)

        current_datetime = timezone.now().date()
        if (
            assignment.time_window_start > current_datetime
            or assignment.time_window_end < current_datetime
        ):
            raise Http404("La ficha no se puede crear en este momento")
        print(form)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        print("Attempting to save Ficha with:")
        print("StudentID:", self.request.user.id)
        print("AssignmentID:", self.kwargs.get("assignment_id"))


class FichaUpdateView(BaseFichaView, UpdateView):
    template_name = "ficha_update.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        button_clicked = self.request.POST.get("submit")

        if button_clicked == "publish":
            # Publish the Ficha
            self.object.status = "Publicado"
        elif button_clicked == "draft":
            # Save as a draft
            self.object.status = "Borrador"
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form data. Please fix the errors below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "Fichas:ficha-detail",
            kwargs={
                "user_id": self.object.student.user.id,
                "assignment_id": self.object.assignment.id,
            },
        )


class FichaDeleteView(BaseFichaView, DeleteView):
    def post(self, request, *args, **kwargs):
        if "confirm_delete" in request.POST:
            return self.delete(request, *args, **kwargs)
        else:
            print("No se borro")
            pass

    def get_success_url(self):
        return reverse_lazy("Fichas:ficha-list")


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
    review = Review.objects.filter(ficha=ficha)
    teacher_has_reviewed = Review.objects.filter(
        ficha=ficha, teacher__user=request.user
    ).exists()
    print(user_id, assignment_id)
    print(ficha.anexos_as_list())
    embed_codes = []
    for anexo in ficha.anexos_as_list():
        try:
            backend = detect_backend(anexo)
            embed_code = backend.get_embed_code(640, 480)
            embed_codes.append(embed_code)
        except UnknownBackendException:
            embed_codes.append({"url": anexo})
    return render(
        request,
        "ficha_detail.html",
        {
            "review": review,
            "ficha": ficha,
            "user_id": user_id,
            "assignment_id": assignment_id,
            "teacher_has_reviewed": teacher_has_reviewed,
            "embed_codes": embed_codes,
        },
    )


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
            print(request.POST)
            new_assignment = form.save()
            print(f"New assignment created: {new_assignment.__dict__}")
            context = {
                "assignment": new_assignment,
                "assignments": assignments,
                "open_assignments": open_assignments,
            }
            if request.htmx:
                return render(
                    request,
                    "components/open_assignment.html",
                    {"assignment": new_assignment},
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


# REVIEWS


def review_create_view(request, user_id, assignment_id):
    teacher = TeacherProfile.objects.get(user=request.user)
    ficha = get_object_or_404(
        Ficha, student__user__id=user_id, assignment__id=assignment_id
    )
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.teacher = teacher
            review.ficha = ficha
            review.save()
            reviews = Review.objects.filter(ficha=ficha)
            rendered = render_to_string(
                "entry.html",
                {
                    "entry": review,
                    "ficha": ficha,
                    "user": request.user,
                    "counter": reviews.count(),
                },
            )
            return HttpResponse(rendered, content_type="text/html")
        # context = {
        #     "form": form,
        #     "ficha": ficha,
        #     "user_id": user_id,
        #     "assignment_id": assignment_id,
        #     "entry": review,
        # }
        # return render(request, "components/review-partial.html", context)

    else:
        form = ReviewForm()
        context = {
            "form": form,
            "ficha": ficha,
            "user_id": user_id,
            "assignment_id": assignment_id,
        }
        return render(request, "review_create_form.html", context)


def review_update_view(request, user_id, assignment_id):
    counter = request.GET.get("counter")
    teacher = TeacherProfile.objects.get(user=request.user)
    ficha = get_object_or_404(
        Ficha, student__user__id=user_id, assignment__id=assignment_id
    )
    review = Review.objects.filter(teacher=teacher, ficha=ficha).first()

    # always create form, either bound to the POST data or unbound
    form = ReviewForm(request.POST or None, instance=review)

    entry = Review.objects.filter(teacher=teacher, ficha=ficha).first()

    if request.method == "POST":
        if form.is_valid():
            if not review:
                review = Review(teacher=teacher, ficha=ficha)
            review.review = form.cleaned_data.get("review")
            review.save()
            return render(
                request,
                "components/review-partial.html",
                {
                    "entry": review,
                    "counter": counter,
                },
            )
    else:
        if review:
            form = ReviewForm(instance=review)
        else:
            form = ReviewForm()

    # always render the form
    return render(
        request,
        "review_update_form.html",
        {"form": form, "ficha": ficha, "counter": counter},
    )


def review_delete_view(request, user_id, assignment_id):
    teacher = TeacherProfile.objects.get(user=request.user)
    ficha = get_object_or_404(
        Ficha, student__user__id=user_id, assignment__id=assignment_id
    )
    review = Review.objects.filter(teacher=teacher, ficha=ficha).first()

    if review is not None:
        review.delete()
        reviews = Review.objects.filter(ficha=ficha)
        rendered = render_to_string(
            "review_list.html",
            {
                "reviews": reviews,
                "ficha": ficha,
                "user": request.user,
                "counter": reviews.count(),
            },
        )
        return HttpResponse(rendered, content_type="text/html")

    else:
        return JsonResponse(
            {"status": "error", "message": "Review does not exist."}, safe=False
        )


def get_entries(request, user_id, assignment_id):
    teacher = TeacherProfile.objects.get(user=request.user)
    ficha = get_object_or_404(
        Ficha, student__user__id=user_id, assignment__id=assignment_id
    )
    reviews = Review.objects.filter(ficha=ficha)
    rendered = render_to_string(
        "review_list.html",
        {
            "reviews": reviews,
            "ficha": ficha,
            "user": request.user,
            "counter": reviews.count(),
        },
    )
    return HttpResponse(rendered, content_type="text/html")
