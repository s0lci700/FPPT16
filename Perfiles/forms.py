from django import forms
from Usuarios.models import CustomUser
from .models import Perfil


class UpdateUserForm(forms.ModelForm):
    pronouns = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Perfil
        fields = ['avatar']
