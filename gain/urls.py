from django.urls import path

from . import views

app_name = 'gains'
urlpatterns = [
    path('<slug:slugParam>/', views.gains, name='gains'),
    path('Todos/<int:id>',
         views.portions, name='allPortions'),
    path('<int:id>', views.portions, name='portions'),
]
