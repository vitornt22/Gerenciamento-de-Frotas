import datetime
import re
from unittest.util import _MAX_LENGTH

from django import forms
from django.core.exceptions import ValidationError
from gain.models import Gain
from Optar import settings

from .models import Location


class LocationForm(forms.ModelForm):
    start_location = forms.DateField(label="Inicio", input_formats=settings.DATE_INPUT_FORMATS,
                                     widget=forms.DateInput(format="%d/%m/%Y", attrs={'readOnly': False, 'id': 'startLocationID', 'data-mask': '99/99/9999'}))
    end_location = forms.DateField(label="Fim", required=False, input_formats=settings.DATE_INPUT_FORMATS, widget=forms.HiddenInput())  # noqa

    class Meta:
        model = Location
        fields = '__all__'

        labels = {
            'start_location': 'Inicio',
            'end_location': 'Fim',
            'id_empresa': 'Empresa',
            'monthly_value': 'Valor Mensal',
            'number_months': 'Nº de Meses'
        }

        widgets = {
            'id': forms.HiddenInput(),
            'empresa_name': forms.HiddenInput(),
            'id_vehicle': forms.HiddenInput(),
            'id_empresa': forms.Select(attrs={'placeholder': 'id_empresa', 'class': 'form-control',  'id': 'id_empresa', 'required': 'True'}),  # noqa
            'number_months': forms.NumberInput(attrs={"placeholder": "Numero de meses",  'required': "True"}),
            'monthly_value': forms.NumberInput(attrs={'placeholder': ' Valor Mensal', 'required': 'True'}),  # noqa
            'total_value': forms.HiddenInput(),
            'id_company': forms.    HiddenInput(),
            'status': forms.HiddenInput(),
            'can_remove': forms.HiddenInput(),


        }

    def clean_start_location(self):
        date = self.cleaned_data.get('start_location')
        edit = self.cleaned_data.get('total_value')
        hoje = datetime.date.today()

        if date < hoje:
            raise ValidationError((
                'Data indisponivel'
            ),
                code='invalid'
            )
        return date

    def clean_number_months(self):
        number = self.cleaned_data.get('number_months')

        if number <= 0:
            raise ValidationError((
                'Não é valido'
            ),
                code='invalid'
            )
        return number


class LocationEditForm(forms.ModelForm):
    start_location = forms.DateField(label="Inicio", required=False,  input_formats=settings.DATE_INPUT_FORMATS,
                                     widget=forms.DateInput(format="%d/%m/%Y", attrs={'name': 'inicio', 'readOnly': False, 'id': 'startLocationID', 'data-mask': '99/99/9999'}))
    end_location = forms.DateField(label="Fim", required=False, input_formats=settings.DATE_INPUT_FORMATS, widget=forms.HiddenInput())  # noqa
    monthly_value = forms.IntegerField(required=False, label="Valor Mensal",  widget=forms.NumberInput(attrs={'readOnly': False, 'id': 'monthID'}))  # noqa

    class Meta:
        model = Location
        fields = '__all__'

        labels = {
            'start_location': 'Inicio',
            'end_location': 'Fim',
            'id_empresa': 'Empresa',
            'number_months': 'Nº de Meses'
        }

        widgets = {
            'id': forms.HiddenInput(),
            'empresa_name': forms.HiddenInput(),
            'id_vehicle': forms.HiddenInput(),
            'id_empresa': forms.Select(attrs={'placeholder': 'id_empresa', 'class': 'form-control', 'id': 'empresaID'}),  # noqa
            'number_months': forms.NumberInput(attrs={"placeholder": "Numero de meses",  'required': "True"}),
            'total_value': forms.HiddenInput(),
            'id_company': forms.    HiddenInput(),
            'status': forms.HiddenInput(),
            'can_remove': forms.HiddenInput(),
        }

    def clean_number_months(self):
        number = self.cleaned_data.get('number_months')

        if number <= 0:
            raise ValidationError((
                'Não é valido'
            ),
                code='invalid'
            )
        return number
