import datetime
import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Vehicle


def license_Plate_validation(lp):
    regex = re.compile(r"^[A-Z]{3}[-][0-9][0-9A-Z][0-9]{2}$")

    if not regex.match(lp) or len(lp) < 8:
        raise ValidationError((
            'Placa no formato indevido'
        ),
            code='invalid'
        )


class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = '__all__'

        labels = {
            'vehicle_type': 'Tipo de Veiculo',
            'year': 'Ano',
            'vehicle_model': 'Modelo',
            'brand': 'Marca',
            'chassi': 'CHASSI',
            'license_plate': 'Placa',
            'it_location': 'it_location'
        }

        help_texts = {
            'chassi': 'Adicione o chassi no padrão correto',
            'license_plate': 'A placa segue o padrão AAA-0000'
        }

        error_messages = {
            'chassi': {
                'required': 'Este campo é obrigatório',
                'invalid': 'Chassi invalido'
            }
        }

        widgets = {
            'it_location': forms.HiddenInput(),
            'vehicle_type': forms.TextInput(attrs={'placeholder': 'Tipo de Veículo', 'name': 'vehicle_type', 'list': 'datalistOptions',
                        'type': '', 'id': 'vehiclesDataList'}),  # noqa
            'year': forms.Select(attrs={'placeholder': 'Ano', 'class': 'form-control'}),  # noqa
            'vehicle_model': forms.TextInput(attrs={'placeholder': 'Modelo do veículo', 'class': 'entrada'}),  # noqa
            'brand': forms.TextInput(attrs={'placeholder': ' Marca', 'class': ''}),  # noqa
            'chassi': forms.TextInput(attrs={'placeholder': 'Chassi', 'class': 'text-uppercase', 'data-mask': '0 AA AAAAAAAA 0 00000', 'minlength': '21'}),  # noqa
            'license_plate': forms.TextInput(attrs={'placeholder': 'Placa do Veículo', 'class': 'text-uppercase', 'data-mask': 'AAA-0A00', 'minlength': '8'}),  # noqa
            'company_user': forms.HiddenInput(),
            'slug': forms.HiddenInput(),

        }

    def clean_year(self):
        year = self.cleaned_data.get('year')

        if len(str(year)) != 4:
            raise ValidationError((
                'Ano indisponivel'
            ),
                code='invalid'
            )
        return year

    def clean_chassi(self):
        chassi = self.cleaned_data.get('chassi')
        regex = re.compile(r"^\d\s\D{2}\s\w{8}\s\d\s\d{5}$")

        if not regex.match(chassi):
            raise ValidationError((
                'Chassi não corresponde ao padrão correto'
            ),
                code='invalid'
            )
        return chassi
