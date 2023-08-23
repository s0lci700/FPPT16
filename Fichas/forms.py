from django import forms
from .models import Ficha, Review


class FichaForm(forms.ModelForm):
    main_image = forms.ImageField(required=False)

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
                attrs={"placeholder": "Título de la ficha", "label": "Título"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Descripción de la ficha",
                    "label": "Descripción",
                }
            ),
            "analysis": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Análisis de la ficha",
                    "label": "Análisis",
                }
            ),
            "references": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Referentes de la obra",
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
