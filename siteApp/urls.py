from django.urls import path

from . import views

app_name = 'site'
urlpatterns = [
    path('', views.home, name='home'),
    path('contato', views.contact, name='contact'),
    path('sobreNós', views.aboutUs, name='aboutUs'),
    path('maquinas', views.vehicles, name='vehicles')
]
