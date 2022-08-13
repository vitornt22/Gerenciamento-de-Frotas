from company.models import Company
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from location.forms import LocationForm
from location.gerarPdf import gerarObj
from location.models import Contract, Location
from vehicle.models import Vehicle

import client_Company
from client_Company.models import Client_company

from .forms import Client_CompanyForm


# Create your views here.
@login_required(login_url='company:login', redirect_field_name='next')
def register_Company(request, id):
    id = int(id)
    if request.POST:
        form = Client_CompanyForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.company_user = request.user
            client.save()
            messages.success(request, 'Locação Cadastrada com Sucesso')
            form = Client_CompanyForm()
        else:
            print("NAO E VALISo")
    else:
        form = Client_CompanyForm()

    profile = str(id)
    if id >= 0:
        active = 1
        previous = Vehicle.objects.get(company_user=request.user, id=id).slug
    else:
        active = 4
        previous = None
    return render(request, "location/cadastroEmpresa.html", {'active': active, 'form': form, 'previous': previous, 'profile': profile})  # noqa


@ login_required(login_url='company:login', redirect_field_name='next')
def listar(request):
    # CONSERTAR ESSA PARTE DO CÓDIGO
    tabela = Client_company.objects.all()

    number = Client_company.objects.filter(
        company_user=request.user).count()
    data = None

    if request.POST.get('inputSearch'):
        data = request.POST.get('inputSearch')

        try:
            if Client_company.objects.filter(company_user=request.user, name__icontains=data).exists():
                tabela = Client_company.objects.filter(company_user=request.user,
                                                       name__icontains=data)
            elif Client_company.objects.filter(company_user=request.user, cnpj__icontains=data).exists():
                tabela = Client_company.objects.filter(company_user=request.user,
                                                       cnpj__icontains=data)
            elif Client_company.objects.filter(company_user=request.user, email__icontains=data).exists():
                tabela = Client_company.objects.filter(company_user=request.user,
                                                       email__icontains=data)
            elif Client_company.objects.filter(company_user=request.user, city__icontains=data).exists():
                tabela = Client_company.objects.filter(company_user=request.user,
                                                       city__icontains=data)
            elif Client_company.objects.filter(company_user=request.user, state__icontains=data).exists():
                tabela = Client_company.objects.filter(company_user=request.user,
                                                       state__icontains=data)
            elif Client_company.objects.filter(company_user=request.user, adress__icontains=data).exists():
                tabela = Client_company.objects.filter(company_user=request.user,
                                                       adress__icontains=data)
            else:
                tabela = None
                data = None
        except:
            tabela = None
            data = None

    return render(request,  'clientes/empresas.html', {'active': 4, 'tag': 'empresas', 'number': number, 'resultados': data, 'tabela': tabela})


@ login_required(login_url='company:login', redirect_field_name='next')
def edit(request, slugParam):
    instancia = Client_company.objects.get(slug=slugParam)
    form = Client_CompanyForm(instance=instancia)

    if request.POST:
        if request.POST.get('voltar'):
            return redirect('clientCompany:empresas')

        form = Client_CompanyForm(request.POST, instance=instancia)
        if form.is_valid():
            form = Client_CompanyForm(request.POST, instance=instancia)
            edit = form.save(commit=False)
            edit.company_user = request.user
            edit.save()

            # atualizando os contratos de locacoes em andamento
            try:
                for i in Location.objects.filter(id_empresa=edit, status=True):
                    if Contract.objects.filter(id_location=i).exists():
                        gerarObj(i)
            except:
                pass

            messages.success(
                request, 'Dados alterados com sucesso!')
            return redirect('clientCompany:empresas')
        else:
            print("AFFF")
    return render(request, 'clientes/EditarClientes.html', {'active': 4, 'form': form, 'client': instancia})  # noqa


@login_required(login_url='company:login', redirect_field_name='next')
def remove(request, slugParam):
    remove = Client_company.objects.get(
        company_user=request.user, slug=slugParam)

    if Location.objects.filter(id_empresa=remove, status=True).exists():
        messages.warning(
            request, "Locação Pendente, empresa nao pode ser excluido")
        return redirect('clientCompany:empresas')

    else:
        remove.delete()
        messages.success(request, "Empresa removida com sucesso")
        return redirect('clientCompany:empresas')
