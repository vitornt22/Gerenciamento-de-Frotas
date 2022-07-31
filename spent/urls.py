from django.urls import path
from location import views as LocView

from . import views

app_name = 'spent'
urlpatterns = [
    path('GastoAdicionado/<slug:slugParam>', views.gastoAdd, name='gastoAdd'),
    path('Gastos/<slug:slugParam>/', views.spents, name='spents'),
    path('Gastos/<slug:slugParam>/<int:id>', views.spentEdit, name='spentEdit'),  # noqa
]
