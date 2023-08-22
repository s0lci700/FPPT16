from django import forms
from .models import CustomUser, StudentProfile


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(
        label="Password", max_length=100, widget=forms.PasswordInput
    )


class CustomUserForm(forms.ModelForm):
    TERCERO = "3"
    CUARTO = "4"
    year_choices = [
        (TERCERO, "Tercer Año"),
        (CUARTO, "Cuarto Año"),
    ]
    year = forms.ChoiceField(choices=year_choices)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "role", "avatar",]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        instance = kwargs.get("instance")
        if instance and instance.studentprofile:
            initial = kwargs.get("initial", {})
            initial["year"] = instance.studentprofile.year
            kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        if not self.user.is_superuser:
            self.fields["role"].disabled = True
            self.fields["year"].disabled = True

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            student_profile, created = StudentProfile.objects.get_or_create(user=user)
            if 'year' in self.cleaned_data and self.cleaned_data["year"]:
                student_profile.year = self.cleaned_data["year"]
                student_profile.save()

        return user
