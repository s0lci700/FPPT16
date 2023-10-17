from django import forms
from .models import Ficha, Review, Assignment, FichaImage, get_default_start_date
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError


class AssignmentForm(forms.ModelForm):
    time_window_start = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
        initial=get_default_start_date,
    )
    time_window_end = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        )
    )

    class Meta:
        model = Assignment
        fields = [
            "title",
            "description",
            "time_window_start",
            "time_window_end",
        ]

    def clean(self):
        cleaned_data = super().clean()
        time_window_start = cleaned_data.get("time_window_start")
        time_window_end = cleaned_data.get("time_window_end")

        if time_window_end < time_window_start:
            msg = "La fecha de cierre no puede ser anterior a la fecha de inicio"
            self.add_error("time_window_end", msg)
        return cleaned_data


# class CustomFileInput(forms.ClearableFileInput):
#     template_name = "components/custom_file_input.html"
#
#
# imgChoices = (
#     ("MAIN", "main"),
#     ("FOTO", "fotograma"),
#     ("COMP", "complementaria"),
#     ("REF", "referencia"),
#     ("O", "otra"),
# )
#
#
# class FichaImageForm(forms.ModelForm):
#     attributes = forms.ChoiceField(
#         choices=imgChoices, label="Tipo de imagen", widget=forms.Select()
#     )
#
#     class Meta:
#         model = FichaImage
#         fields = ["image", "attributes"]
#         widgets = {
#             "image": CustomFileInput(),
#         }
#
#
# # add a fichaimage inlineformset to fichaform


class FichaForm(forms.ModelForm):
    main_image = forms.ImageField()

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
            "anexos",
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
            "anexos": forms.URLInput(
                attrs={"class": "url-input", "placeholder": "URL"}
            ),
            # specify other field widgets here...
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(FichaForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial["keywords"] = ", ".join(
                [kw.name for kw in self.instance.keywords.all()]
            )

    def save(self, commit=True):
        instance = super(FichaForm, self).save(commit=False)

        if commit:
            instance.save()

        if instance.pk:
            instance.keywords.clear()  # clear old keywords
            keywords = self.cleaned_data["keywords"]
            # Check if keywords is a string or a list and then handle it accordingly
            if isinstance(keywords, str):
                keywords = keywords.split(",")
            for keyword in keywords:
                instance.keywords.add(keyword.strip())  # add new keywords

        return instance


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]
        widgets = {
            "review": forms.Textarea(attrs={"rows": 3}),
        }
