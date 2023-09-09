from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .forms import CustomUserForm
from .models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserForm
    model = CustomUser
    template_name = "register_view.html"

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class EditUser(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = "edit_user.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.htmx:
            print("Htmx")
            super().get(request, *args, **kwargs)
            return render(
                request, "components/user_edit_form.html", {"form": self.get_form()}
            )
        else:
            print("Not Htmx")
            super().get(request, *args, **kwargs)
            return render(request, "edit_user.html", {"form": self.get_form()})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if request.htmx:
            print("Htmx")
            if form.is_valid():
                form.save()
                return redirect("Cuentas:user_detail", pk=self.object.pk)
            else:
                print("Not Htmx")
                if form.is_valid():
                    form.save()
                    return redirect("Cuentas:user_detail", pk=self.object.pk)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(pk=self.object.pk)
        context["user"] = user
        return context

    def get_success_url(self):
        return reverse_lazy("Cuentas:user_detail", kwargs={"pk": self.object.pk})

    def get_initial(self):
        initial = super().get_initial()
        self.object = self.get_object()
        initial["email"] = self.object.email
        initial["role"] = self.object.role
        initial["birth_date"] = self.object.birth_date
        # initial["year"] = self.object.year
        return initial

    def form_valid(self, form):
        print("Form is valid")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is not valid", form.errors)
        return super().form_invalid(form)


class DeleteUser(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = CustomUser
    success_url = reverse_lazy("landing")
    template_name = "user_confirm_delete.html"

    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, "User deleted.")
        return super().delete(request, *args, **kwargs)
