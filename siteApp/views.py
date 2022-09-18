from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'site/index.html')


def contact(request):
    return render(request, 'site/contacts.html')


def aboutUs(request):
    return render(request, 'site/about.html')


def vehicles(request):
    return render(request, 'site/vehicles.html')
