from django.shortcuts import render
from .forms import FichaForm


# Create your views here.
def ficha_general_view(request):
    return render(request, 'ficha.html')


def ficha_create_view(request):
    if request.method == 'POST':
        form = FichaForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FichaForm()

    return render(request, 'ficha_create.html', {'form': form})


def ficha_detail_view(request):
    return render(request, 'ficha.html')


def ficha_update_view(request):
    return render(request, 'ficha.html')


def ficha_delete_view(request):
    return render(request, 'ficha.html')
