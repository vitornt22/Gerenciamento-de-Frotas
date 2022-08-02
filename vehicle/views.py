import datetime
from operator import add

from client_Company.forms import Client_CompanyForm
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from gain.addGains import addGains
from gain.models import Gain
from location.forms import LocationForm
from location.gerarPdf import gerarObj
from location.models import Contract, Location
from Optar import settings as varoptar
from report.models import Report
from spent.forms import SpentForm
from spent.models import Spent

from vehicle.forms import VehicleForm

from .funcoes import calculateNumberMonths
from .models import Vehicle, Vehicle_Types


# Create your views here.
def check_dates(vehicle, request):

    # Checando locações que chegaram ao fim na data corrente
    for i in vehicle:
        loc = Location.objects.filter(
            id_company=request.user, id_vehicle=i, status=True)
        for j in loc:
            if j.end_location == datetime.date.today():
                j.status = False
                j.can_remove = False
                i.it_location = False
                j.save()
                i.save()


@login_required(login_url='company:login', redirect_field_name='next')
def index(request):
    print("DEBUGG", varoptar.DEBUG)
    print("DATABASE", varoptar.DATABASES['default']['ENGINE'])
    vehicle = Vehicle.objects.filter(company_user=request.user)
    check_dates(vehicle, request)
    tabela = Vehicle.objects.filter(
        company_user=request.user).order_by('-created_at')
    number = Vehicle.objects.filter(company_user=request.user).count()
    resultados = None

    if request.POST.get("inputSearch"):
        valida = request.POST.get("inputSearch")
        resultados = valida
        print("VALIDAA: ", valida)

        if Vehicle.objects.filter(company_user=request.user, vehicle_type__iexact=valida).exists():
            tabela = Vehicle.objects.filter(
                company_user=request.user, vehicle_type__iexact=valida).order_by('-created_at')
            print("EXISTE O TIPO")
        elif Vehicle.objects.filter(company_user=request.user, vehicle_model__iexact=valida).exists():
            tabela = Vehicle.objects.filter(
                company_user=request.user, vehicle_model__iexact=valida).order_by('-created_at')
        elif Vehicle.objects.filter(company_user=request.user, year__iexact=valida).exists():
            tabela = Vehicle.objects.filter(
                company_user=request.user, year=valida)
        elif Vehicle.objects.filter(company_user=request.user,  brand__iexact=valida).exists():
            tabela = Vehicle.objects.filter(
                company_user=request.user, brand__iexact=valida).order_by('-created_at')
        elif Vehicle.objects.filter(company_user=request.user,  chassi__iexact=valida).exists():
            tabela = Vehicle.objects.filter(
                company_user=request.user, chassi__iexact=valida).order_by('-created_at')
        elif Vehicle.objects.filter(company_user=request.user,  license_plate__iexact=valida).exists():
            tabela = Vehicle.objects.filter(
                company_user=request.user, license_plate__iexact=valida).order_by('-created_at')
        elif len(valida) > 0:
            tabela = None
            resultados = None
        else:
            tabela = Vehicle.objects.filter(company_user=request.user)

    profileParam = "veiculos"

    return render(request, "vehicle/veiculos.html", {'active': 1, 'profile': profileParam, 'tabela': tabela, 'resultados': resultados, 'number': number})


@login_required(login_url='company:login', redirect_field_name='next')
def remove(request, slugParam):

    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    remove = Vehicle.objects.filter(slug=slugParam)
    if Location.objects.filter(id_vehicle=vehicle, status=True).exists():
        messages.warning(
            request, "Locação Pendente, veículo nao pode ser excluido")
        if "Veiculos" not in request.path:
            return redirect('vehicle:profile', slugParam)
    else:
        remove.delete()
        messages.success(request, "Veiculo removido com sucesso")

    return redirect('vehicle:one')


@login_required(login_url='company:login', redirect_field_name='next')
def profile(request, slugParam):
    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    spents = Spent.objects.filter(id_vehicle=vehicle)
    locations = Location.objects.filter(id_vehicle=vehicle)
    gains = Gain.objects.filter(
        id_vehicle=vehicle, date__year=datetime.date.today().year)
    form = VehicleForm(instance=vehicle)
    addSpent = SpentForm()
    profileParam = str(vehicle.license_plate)

    if request.POST:
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.company_user = request.user
            edit.slug = f'{slugify(edit.chassi)}'
            edit.save()
            slugParam = edit.slug

            for i in Location.objects.filter(id_vehicle=edit, status=True):
                if Contract.objects.filter(id_location=i).exists():
                    print("Existe locacao")
                    gerarObj(i)
            messages.success(
                request, 'Dados alterados com sucesso com Sucesso')

    return render(request, 'vehicle/vehicleProfile.html', {'active': 1, 'gains': gains, 'locations': locations, 'spents': spents, 'spentForm': addSpent, 'form': form, 'profile': profileParam, 'vehicle': vehicle, 'slug': slugParam})  # noqa


@login_required(login_url='company:login', redirect_field_name='next')
def register_vehicle(request):
    types = Vehicle_Types.objects.filter(company_user=request.user)
    if request.POST:
        form = VehicleForm(request.POST)
        if form.is_valid():
            register = form.save(commit=False)
            types_reg = Vehicle_Types()
            types_reg.company_user = request.user
            types_reg.types = request.POST.get('vehicle_type')
            register.vehicle_type = request.POST.get('vehicle_type')
            register.company_user = request.user
            print("REQUEST USER ", request.user)
            register.save()
            messages.success(request, 'Veiculo Cadastrado com Sucesso')
            form = VehicleForm()
    else:
        print("NAO E VALIDO")
        form = VehicleForm()
    return render(request, 'vehicle/cadastroVeiculo.html', {'active': 1, 'form': form, 'types': types})


@ login_required(login_url='company:login', redirect_field_name='next')
def edit(request, slugParam):
    instancia = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    form = VehicleForm(instance=instancia)
    print("USUARIOOO:", request.user)
    user = request.user
    types = Vehicle_Types.objects.filter(company_user=user)

    if request.POST:

        if request.POST.get('voltar'):
            return redirect('vehicle:indexVehicle')

        form = VehicleForm(request.POST, instance=instancia)
        if form.is_valid():
            print('OLÀAAAA')
            edit = form.save(commit=False)
            edit.company_user = request.user
            edit.slug = f'{slugify(edit.chassi)}'
            edit.save()
            slugParam = edit.slug

            # atualizando os contratos de locacoes em andamento
            try:
                for i in Location.objects.filter(id_vehicle=edit, status=True):
                    if Contract.objects.filter(id_location=i).exists():
                        print("Existe locacao")
                        gerarObj(i)
            except:
                pass

            messages.success(
                request, 'Dados alterados com sucesso com Sucesso')
            return redirect('vehicle:edit', edit.slug)
        else:
            print("AFFF")
    return render(request, 'vehicle/edit.html', {'active': 1, 'form': form, 'types': types, 'slug': slugParam})  # noqa
