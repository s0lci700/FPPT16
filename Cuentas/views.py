from django.conf import settings
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import resolve
from django.views.generic import DetailView, ListView
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from taggit.models import Tag
from PIL import Image
from io import BytesIO
import io
from django.http import FileResponse
from django.core.files.storage import default_storage as storage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.conf import settings

settings.BASE_URL = "http://localhost:8000/"  # add your actual domain here

from Fichas.models import Ficha
from .models import CustomUser
import requests

User = get_user_model()


# General List View with logic for different roles
class UserListView(ListView):
    """
    UserListView

    A class-based view for displaying a list of users with different roles.

    Attributes:
    - context_object_name: The name of the variable to be used in the template to refer to the user list.
    - context: A dictionary containing the different user roles as keys and corresponding user objects as values.

    Methods:
    - get_template_names(): Returns the template name based on the role parameter specified in the URL.
    - get_queryset(): Returns the queryset of users based on the role parameter specified in the URL.
    - get_context_data(**kwargs): Adds additional context to the default context_data method.

    Example Usage:
    ```python
    user_list_view = UserListView.as_view()
    ```
    """

    context_object_name = "users"
    context = {
        "alumni": CustomUser.objects.filter(role="A"),
        "profesores": CustomUser.objects.filter(role="P"),
        "otros": CustomUser.objects.filter(role="NS"),
    }

    def get_template_names(self):
        role = self.kwargs.get("role")
        return f"{role}.html"

    def get_queryset(self):
        role = self.kwargs.get("role")

        if role == "all_users":
            return CustomUser.objects.all()

        role_mapping = {
            "alumni": "A",
            "profesores": "P",
        }

        return CustomUser.objects.filter(role=role_mapping[role])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs["role"] not in ["alumni", "profesores"]:
            users = context["users"]
            context["alumni"] = [user for user in users if user.role == "A"]
            context["profesores"] = [user for user in users if user.role == "P"]
            context["otros"] = [user for user in users if user.role not in ["A", "P"]]

        return context


# Detail views
def user_detail_redirect(request, pk):
    """
    Redirects the user detail page based on the role of the user.

    :param request: The HTTP request object.
    :param pk: The primary key of the user.
    :return: A redirect response to the appropriate user detail page.

    """
    user = get_object_or_404(CustomUser, pk=pk)
    if user.role == "A":
        return redirect("Cuentas:student_detail", pk=pk)
    elif user.role == "P":
        return redirect("Cuentas:teacher_detail", pk=pk)


class UserDetailView(DetailView):
    """
    Class UserDetailView

    A view that displays detailed information about a user.

    Inherits From:
        - django.views.generic.DetailView

    Attributes:
        - model (CustomUser): The model class to use for retrieving the user object.
        - template_name (str): The name of the template used to render the view.

    Methods:
        - get_object(queryset=None): Retrieves the user object based on the URL name and primary key.
        - get_context_data(**kwargs): Adds additional context data to be used in the template.

    """

    model = CustomUser
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        user = super().get_object(queryset=queryset)
        print("PK: ", pk)
        print("User: ", user)

        # Determine the role based on the URL name
        url_name = resolve(self.request.path_info).url_name
        if url_name == "student_detail":
            return get_object_or_404(CustomUser, pk=pk, role="A")
        elif url_name == "teacher_detail":
            return get_object_or_404(CustomUser, pk=pk, role="P")
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Print the information of the user in the current session
        session_user = get_user(self.request)
        print("Viewed User: ", self.object)
        print("Session User: ", session_user, session_user.pk, session_user.role)
        if self.object.role == "A":
            student_profile = self.object.studentprofile
            user_fichas = student_profile.user_ficha.all()
            tags = Tag.objects.filter(ficha__in=user_fichas).distinct()
            context["tags"] = tags
            context["user_fichas"] = user_fichas
            student = CustomUser.objects.get(pk=self.object.pk)
            context["student"] = student
        elif self.object.role == "P":
            teacher_profile = self.object.teacherprofile
            context["teacher"] = teacher_profile
        return context


from django.http import FileResponse


def get_dossier(request, pk):
    active_user = request.user.pk
    user = CustomUser.objects.get(pk=active_user)
    if user.role == "A":
        student_profile = user.studentprofile
        fichas = Ficha.objects.filter(student=student_profile).all()
        c = canvas.Canvas("dossier.pdf", pagesize=letter)

        width, height = letter

        c.setFont("Helvetica", 14)
        c.drawString(
            2 * cm,
            height - 2 * cm,
            f"{student_profile.user.first_name} {student_profile.user.last_name}",
        )
        height -= 1.2 * 14

        for i, ficha in enumerate(fichas):
            response = requests.get(settings.BASE_URL + ficha.main_image.url)
            img = Image.open(BytesIO(response.content))
            img_path = ficha.main_image.path
            if not settings.DEBUG:
                image_file = storage.open(img_path, "rb")
                image = ImageReader(BytesIO(image_file.read()))
                image_file.close()
            else:
                image = ImageReader(img_path)

            if i != 0:
                c.showPage()

            c.drawString(2 * cm, height - 2 * cm, f"Ficha {i+1}: {ficha.title}")

            size = 12
            height -= 2 * cm + size
            line_height = 1.2 * size

            c.setFont("Helvetica", size)

            c.drawString(
                2 * cm, height - line_height, f"Descripcion: {ficha.description}"
            )
            height -= line_height

            c.drawString(
                2 * cm, height - line_height, f"Analisis Operacional: {ficha.analysis}"
            )
            height -= line_height

            c.drawString(
                2 * cm,
                height - line_height,
                f"Analisis Referencial: {ficha.references}",
            )
            height -= line_height

            if ficha.misc:
                c.drawString(2 * cm, height - line_height, f"Miscelaneo: {ficha.misc}")
                height -= line_height

            if ficha.anexos:
                c.drawString(2 * cm, height - line_height, f"Anexos: {ficha.anexos}")
                height -= line_height

            for keyword in ficha.keywords.all():
                c.drawString(2 * cm, height - line_height, f"{keyword}")
                height -= line_height

            img_width = width - 4 * cm  # define image width as you want
            aspect = image.getSize()[1] / float(
                image.getSize()[0]
            )  # calc aspect ratio of image
            img_height = aspect * img_width  # calc image height based on aspect ratio
            c.drawImage(
                image,
                2 * cm,
                height - img_height - 2 * cm,
                width=img_width,
                height=img_height,
            )

        c.save()

        # Open the saved file and send it as a response
        file = open("dossier.pdf", "rb")
        response = FileResponse(file, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="dossier.pdf"'
        return response
    else:
        return Http404


class MyFichasViews(ListView, LoginRequiredMixin):
    """

    This class represents a view for displaying a list of Fichas objects belonging to the logged-in user.

    :class: MyFichasViews
    :inherits: ListView, LoginRequiredMixin

    Attributes:
        - model (Ficha): specifies the model class to use for retrieving the Ficha objects.
        - template_name (str): the name of the template to use for rendering the list view.
        - context_object_name (str): the name to use for the list of Ficha objects in the template context.

    Methods:
        - get_queryset(): returns a queryset of Ficha objects belonging to the logged-in user.

    """

    model = Ficha
    template_name = "ficha_list.html"
    context_object_name = "fichas"

    def get_queryset(self):
        active_user = self.request.user.pk
        user = CustomUser.objects.get(pk=active_user)
        if user.role == "A":
            student_profile = user.studentprofile
            return Ficha.objects.filter(student=student_profile).all()
        else:
            raise Http404
