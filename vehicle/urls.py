from django.urls import path
from location import views as LocView

from . import views

app_name = 'vehicle'
urlpatterns = [
    path('', views.index, name='indexVehicle'),
    path('', views.index, name='one'),
    path('cadastroVeiculo/', views.register_vehicle, name='regVehicle'),
    path('<slug:slugParam>', views.edit, name='edit'),
    path('<slug:slugParam>/remove', views.remove, name='remove'),
    path('Veiculos/<slug:slugParam>/remove>', views.remove, name='removeAll'),
    path('profile/<slug:slugParam>', views.profile, name='profile'),
]
