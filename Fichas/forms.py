from django import forms
from .models import Ficha, Review


class FichaForm(forms.ModelForm):
    class Meta:
        model = Ficha
        fields = ['student', 'title', 'main_image', 'complementary_images', 'description', 'analysis', 'references',
                  'keywords', 'misc']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['teacher', 'ficha', 'review']
