from operator import add

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from gain.addGains import addGains
from location.models import Location
from report.models import Report
from vehicle.models import Vehicle

from .forms import SpentForm
from .models import Spent


@login_required(login_url='company:login', redirect_field_name='next')
def spentEdit(request, slugParam, id):
    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    spent = Spent.objects.get(id_vehicle=vehicle, id=id)
    spentForm = SpentForm(instance=spent)

    if request.POST:
        spentForm = SpentForm(request.POST, instance=spent)
        if spentForm.is_valid():
            print("ENTROUUU")
            edit = spentForm.save(commit=False)
            edit.id_company = request.user
            edit.id_vehicle = vehicle
            edit.save()
            messages.success(request, 'Gasto editado com sucesso')
        else:
            print("NAO ENTROU")
    return render(request, 'spent/EditarGasto.html', {'active': 1, 'spent': spent, 'include': 1,  'id': id, 'slug': slugParam, 'vehicle': vehicle, 'form': spentForm})  # noqa


@login_required(login_url='company:login', redirect_field_name='next')
def spents(request, slugParam):
    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    tabela = Spent.objects.filter(id_vehicle=vehicle).order_by('-date')
    number = Spent.objects.filter(id_vehicle=vehicle).count()
    data = None
    tag = "Gastos"

    if request.POST.get('inputSearch'):
        data = request.POST.get('inputSearch')
        try:
            if Spent.objects.filter(id_vehicle=vehicle, date__icontains=data).exists():
                tabela = Spent.objects.filter(id_vehicle=vehicle,
                                              date__icontains=data)
            elif Spent.objects.filter(id_vehicle=vehicle, occasion__icontains=data).exists():
                tabela = Spent.objects.filter(id_vehicle=vehicle,
                                              occasion__icontains=data)
            elif Spent.objects.filter(id_vehicle=vehicle, valor__icontains=data).exists():
                tabela = Spent.objects.filter(id_vehicle=vehicle,
                                              valor__icontains=data)
            else:
                tabela = None
                data = None
        except:
            tabela = None
            data = None

    a = request.POST.get('removerTableButton')
    print("VALOR DE A", a)

    if request.POST.get('removerTableButton'):
        remove = Spent.objects.filter(id_vehicle=vehicle, id=a)
        remove.delete()

    return render(request, 'spent/gastos.html', {'active': 1, 'include': 1, 'tag': tag, 'number': number, 'resultados': data, 'slug': slugParam, 'vehicle': vehicle,  'tabela': tabela})


@login_required(login_url='company:login', redirect_field_name='next')
def gastoAdd(request, slugParam):
    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    form = SpentForm(request.POST)

    if request.POST:
        if form.is_valid():
            form = SpentForm(request.POST)
            register = form.save(commit=False)
            register.id_vehicle = vehicle
            register.id_company = request.user
            register.save()
            icon = "success"
            messages.success(request, "Gasto Adicionado com sucesso")
            if Report.objects.filter(id_company=request.user, year=register.date.year,  month=register.date.month).exists() is False:
                report = Report()
                report.year = register.date.year
                report.month = register.date.month
                report.id_company = request.user
                report.save()
        else:
            icon = "error"
            messages.error(request, "Erro ao adicionar gasto, data invalida")
    else:
        form = SpentForm()
    return redirect('vehicle:profile', slugParam)
