from django import forms
from .models import Ficha, Review, Assignment, FichaImage
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.forms import modelformset_factory


class AssignmentForm(forms.ModelForm):
    time_window_start_date = forms.DateField(
        widget=AdminDateWidget(
            attrs={
                "format": format("%d/%m/%Y"),
                "type": "date",
            }
        )
    )
    time_window_end_date = forms.DateField(
        widget=AdminDateWidget(
            attrs={
                "format": format("%d/%m/%Y"),
                "type": "date",
            }
        )
    )

    class Meta:
        model = Assignment
        fields = [
            "title",
            "description",
            "time_window_start_date",
            "time_window_end_date",
        ]


class CustomFileInput(forms.ClearableFileInput):
    template_name = "components/custom_file_input.html"


imgChoices = (
    ("MAIN", "main"),
    ("FOTO", "fotograma"),
    ("COMP", "complementaria"),
    ("REF", "referencia"),
    ("O", "otra"),
)


class FichaImageForm(forms.ModelForm):
    attributes = forms.ChoiceField(
        choices=imgChoices, label="Tipo de imagen", widget=forms.Select()
    )

    class Meta:
        model = FichaImage
        fields = ["image", "attributes"]
        widgets = {
            "image": CustomFileInput(),
        }


# add a fichaimage inlineformset to fichaform


class FichaForm(forms.ModelForm):
    main_image = forms.ImageField(widget=CustomFileInput)

    class Meta:
        model = Ficha
        exclude = ["student", "status", "created_at", "updated_at"]
        fields = [
            "title",
            "main_image",
            "description",
            "analysis",
            "references",
            "keywords",
            "misc",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "rows": 2,
                    "placeholder": "Título de la ficha",
                    "label": "Título",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Descripción de la ficha",
                    "label": "Descripción",
                }
            ),
            "analysis": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Análisis Operacional",
                    "label": "Análisis",
                }
            ),
            "references": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Analisis Referencial",
                    "label": "Referentes",
                }
            ),
            "misc": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "Información adicional",
                    "label": "Información adicional",
                }
            ),
            "keywords": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "Palabras clave",
                    "label": "Palabras clave",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(FichaForm, self).__init__(*args, **kwargs)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["teacher", "ficha", "review"]
        widgets = {
            "review": forms.Textarea(attrs={"rows": 5}),
        }
