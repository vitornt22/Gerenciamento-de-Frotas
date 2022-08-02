from django import forms
from django.core.exceptions import ValidationError

from .models import Client_company


class Client_CompanyForm(forms.ModelForm):

    class Meta:
        model = Client_company
        fields = '__all__'

        error_messages = {
            'cnpj': {'required': 'Este campo é obrigatório', 'unique': ' Este cnpj ja existe'},  # noqa
            'state': {'required': 'Este campo é obrigatório', 'class': 'form-control'},  # noqa
            'contact': {'required': 'Este campo é obrigatório', },  # noqa
            'name': {'required': 'Este campo é obrigatório', },  # noqa
            'email': {'required': 'Este campo é obrigatório', 'unique': 'Este email já existe'},  # noqa
            'adress': {'required': 'Este campo é obrigatório', },  # noqa
            'district': {'required': 'Este campo é obrigatório', },  # noqa
            'city': {'required': 'Este campo é obrigatório', },  # noqa

        }

        labels = {
            'cnpj': 'CNPJ',
            'state': 'Estado',
            'name': 'Nome da Empresa',
            'contact': 'Telefone',
            'email': 'Email da Empresa',
            'adress': 'Endereço da Empresa',
            'district': 'Bairro da Empresa',
            'zip_code': 'CEP',
            'number': 'Nº',
            'city': 'Cidade'
        }

        widgets = {

            'cnpj': forms.TextInput(attrs={'placeholder': 'CNPJ da empresa', 'data-mask': '99.999.999/9999-99'}),  # noqa
            'company_user': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'placeholder': ' Nome da Empresa', 'required': 'True'}),  # noqa
            'contact': forms.TextInput(attrs={'placeholder': ' Telefone', 'data-mask': '(99) 99999-9999'}),  # noqa
            'email': forms.EmailInput(attrs={'placeholder': 'Email da Empresa'}),  # noqa
            'adress': forms.TextInput(attrs={'placeholder': 'Endereço da empresa'}),
            'number': forms.NumberInput(attrs={'placeholder': ' Nº', 'required': "True"}),
            'district': forms.TextInput(attrs={'placeholder': 'Bairro da empresa'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'CEP da Empresa', 'data-mask': '99999-999'}),  # noqa
            'city': forms.TextInput(attrs={'placeholder': 'Cidade'}),
            'state': forms.Select(attrs={'placeholder': 'Estado'}),
            'slug': forms.HiddenInput()

        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')

        if len(cnpj) != 18:
            raise ValidationError((
                'CNPJ menor do que o devido'
            ),
                code='invalid'
            )
        return cnpj
