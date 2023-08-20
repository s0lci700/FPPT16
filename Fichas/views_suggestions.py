from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ficha
from .forms import FichaForm

class FichaCreateUpdateDeleteView(LoginRequiredMixin, CreateView, UpdateView, DeleteView):
    model = Ficha
    template_name = 'fichas/ficha_form.html'
    form_class = FichaForm

    def get_object(self, queryset=None):
        if self.kwargs.get('pk'):
            return super().get_object(queryset)
        return None

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            return render(request, 'fichas/ficha_delete_confirm.html', {'ficha': self.get_object()})
        elif 'confirm_delete' in request.POST:
            # Check password confirmation here
            if request.user.check_password(request.POST['password']):
                return self.delete(request, *args, **kwargs)
            else:
                return render(request, 'fichas/ficha_delete_confirm.html', {'ficha': self.get_object(), 'error': 'Incorrect password'})
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        ficha = form.save(commit=False)
        if 'save_draft' in self.request.POST:
            ficha.status = 'draft'
        else:
            ficha.status = 'published'
        ficha.student = self.request.user.studentprofile
        ficha.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ficha-list') # Redirect to the list of fichas after successful action


##URL.py suggestion
from django.urls import path
from .views import FichaCreateUpdateDeleteView, ficha_general_view

urlpatterns = [
    path('fichas/', ficha_general_view, name='ficha-list'),
    path('fichas/create/', FichaCreateUpdateDeleteView.as_view(), name='ficha-create'),
    path('fichas/<int:pk>/', FichaCreateUpdateDeleteView.as_view(), name='ficha-detail'),
    path('fichas/<int:pk>/update/', FichaCreateUpdateDeleteView.as_view(), name='ficha-update'),
    path('fichas/<int:pk>/delete/', FichaCreateUpdateDeleteView.as_view(), name='ficha-delete'),
]
