from django.urls import path

from . import views

app_name = 'location'
urlpatterns = [
    path('', views.index),
    path('<slug:slugParam>',  views.locations, name='locations'),
    path('locar/<slug:slugParam>/<str:profileParam>', views.locar, name='locar'),
    path('<int:id>/pdf',  views.gerarContrato, name='pdf'),
    path('Todos/',  views.loc, name='allLocations'),
    path('<slug:slugParam>/', views.locations, name='locations'),
    path('<slug:slugParam>/<int:id>',  views.edit, name='edit'),
    path('Todos/<slug:slugParam>/<int:id>',  views.edit, name='editAll'),
    path('Todas/<slug:slugParam>/<int:id>/remove',
         views.remove, name='removeAll'),
    path('<slug:slugParam>/<int:id>/remove',
         views.remove, name='remove'),



]
