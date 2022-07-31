import datetime
import re

from dateutil.relativedelta import relativedelta
from django import forms
from django.core.exceptions import ValidationError
from Optar import settings
from vehicle.models import Vehicle

from .models import Spent


class SpentForm(forms.ModelForm):
    occasion = forms.CharField(label="Ocasião do Gasto",
                               required=True, widget=forms.TextInput(attrs={'type': '', 'rows': 4, 'cols': 40}))
    date = forms.DateField(label="Data do Gasto", required=True, input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={'data-mask': '99/99/9999'}))  # noqa

    class Meta:
        model = Spent
        fields = '__all__'

        labels = {
            'valor': 'Valor do Gasto',
        }

        error_messages = {
            'valor': {
                'required': 'Este campo é obrigatório',
                'invalid': 'Chassi invalido'
            }
        }

        widgets = {
            'id_vehicle': forms.HiddenInput(attrs={'placeholder': 'id do veiculo'}),
            'valor': forms.NumberInput(),
            'id_company': forms.HiddenInput(),

        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        hoje = datetime.date.today()
        if date > hoje or date.year != hoje.year or date.month != hoje.month:
            raise ValidationError((
                'Nao pode adicionar gastos futuros',
                'Os Gastos devem ser desse ano',
            ),
                code='invalid'
            )
        return date
