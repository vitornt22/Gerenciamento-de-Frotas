from company.models import Company
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import  redirect, render
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
    tabela = Client_company.objects.filter(
        company_user=request.user)

    number = Client_company.objects.filter(
        company_user=request.user).count()

    data = request.GET.get('inputSearch')
    if data:
        tabela = Client_company.objects.filter(
            Q(company_user=request.user) & Q(Q(name__icontains=data) | Q(cnpj__icontains=data) | Q(  # noqa
                email__icontains=data) | Q(city__icontains=data) | Q(state__icontains=data) | Q(adress__icontains=data)))  # noqa

        if tabela.count() == 0:
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
