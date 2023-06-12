
import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.text import slugify
from location.models import Location
from report.models import Report
from vehicle.models import Vehicle

from .addGains import addGains
from .models import Gain

# Create your views here.


@login_required(login_url='company:login', redirect_field_name='next')
def portions(request, id):

    tabela = Gain.objects.filter(id_location=id).order_by('it_paid', 'date')
    number = Gain.objects.filter(id_location=id).count()
    data = None

    try:
        slug = Location.objects.get(id=id).id_vehicle.slug
    except:
        slug = None

    # Checar se esta na aba de veiculos ou locação
    if "Todos/" in request.path:
        include = 2
        active = 2
        portionTag = 'gains:allPortions'
        prev = 'location:allLocations'
    else:
        active = 1
        include = 1
        portionTag = 'gains:portions'
        prev = 'location:locations'

    location = Location.objects.get(id=id)
    tag = "Parcelas"

    if request.POST.get('inputSearch'):
        data = request.POST.get('inputSearch')
        try:
            if Gain.objects.filter(id_location=id,  date__icontains=data).exists():
                tabela = Gain.objects.filter(id_location=id,
                                             date__icontains=data)
            elif Gain.objects.filter(id_location=id, occasion__icontains=data).exists():
                tabela = Gain.objects.filter(id_location=id,
                                             occasion__icontains=data)
            elif Gain.objects.filter(id_location=id, valor__icontains=data).exists():
                tabela = Gain.objects.filter(id_location=id,
                                             valor__icontains=data)
            else:
                tabela = None
                data = None
        except:
            tabela = None
            date = None

    if request.POST.get('its_Paid'):
        id = request.POST.get('its_Paid')
        gain = Gain.objects.get(
            id_location=location, id=id)
        gain.it_paid = True
        gain.can_pay = False
        date = gain.date + relativedelta(months=1)

        # Verificar se não  existe relatório do mês corrente
        if not Report.objects.filter(id_company=request.user, year=gain.date.year,  month=gain.date.month).exists():
            report = Report()
            report.year = gain.date.year
            report.month = gain.date.month
            report.id_company = request.user
            report.save()

        # Possibilitar que o próximo ganho possa ser pago
        try:
            nextGain = Gain.objects.get(
                id_location=location, date=date)
            nextGain.can_pay = True
            nextGain.save()
        except:
            pass

        gain.save()

        pagos = Gain.objects.filter(
            id_company=request.user, id_location=location, it_paid=True)

        if pagos.count() == location.number_months:
            location.can_remove = False
        else:
            location.can_remove = True

        location.save()

        messages.warning(
            request, "Tem certeza que deseja adicionar como pago?")

    return render(request, 'gain/ganhos.html', {'portionTag': portionTag, 'active': active, 'slug': slug, 'include': include, 'prev': prev, 'tag': tag, 'number': number, 'resultados': data,  'tabela': tabela})


@login_required(login_url='company:login', redirect_field_name='next')
def gains(request, slugParam):
    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    tabela = Gain.objects.filter(
        id_vehicle=vehicle, it_paid=True).order_by('it_paid', 'date')
    number = Gain.objects.filter(id_vehicle=vehicle).count()
    data = None
    tag = "Ganhos"

    if request.POST.get('inputSearch'):
        data = request.POST.get('inputSearch')
        try:
            if Gain.objects.filter(id_vehicle=vehicle, it_paid=True, date__icontains=data).exists():
                tabela = Gain.objects.filter(id_vehicle=vehicle, it_paid=True,
                                             date__icontains=data)
            elif Gain.objects.filter(id_vehicle=vehicle, it_paid=True, occasion__icontains=data).exists():
                tabela = Gain.objects.filter(id_vehicle=vehicle, it_paid=True,
                                             occasion__icontains=data)
            elif Gain.objects.filter(id_vehicle=vehicle, it_paid=True, valor__icontains=data).exists():
                tabela = Gain.objects.filter(id_vehicle=vehicle, it_paid=True,
                                             valor__icontains=data)
            else:
                tabela = None
                data = None
        except:
            tabela = None
            data = None


    return render(request, 'gain/ganhos.html', {'active': 1, 'portionTag': 'gains:portions', 'include': 1, 'tag': tag, 'number': number, 'resultados': data, 'slug': slugParam, 'vehicle': vehicle,  'tabela': tabela})
