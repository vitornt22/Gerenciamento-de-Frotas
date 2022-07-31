from django.urls import path

from client_Company import views

app_name = 'clientCompany'
urlpatterns = [
    path('CadastroEmpresa/<str:id>', views.register_Company, name='register'),
    path('', views.listar, name='empresas'),
    path('Editar/<slug:slugParam>', views.edit, name='edit'),
    path('Remover/<slug:slugParam>', views.remove, name='remove'),

]
