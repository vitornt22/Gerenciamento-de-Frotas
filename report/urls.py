from django.urls import path

from . import views

app_name = 'report'
urlpatterns = [
    path('', views.reports, name='all'),
    path('<int:id>/pdf',  views.gerarRelatorioView, name='pdf'),



]
