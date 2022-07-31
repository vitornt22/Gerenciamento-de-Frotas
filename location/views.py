import datetime
import io
from logging import exception

from company.models import Company
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import ValidationError
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from gain.addGains import addGains, removeGains
from gain.models import Gain
from reportlab.pdfgen import canvas
from spent.models import Spent
from vehicle.models import Vehicle

from .forms import LocationEditForm, LocationForm
from .gerarPdf import createPdf, gerarObj
from .models import Contract, Location


# Create your views here.
@login_required(login_url='company:login', redirect_field_name='next')
def index(request):
    return render(request, 'locacoes.html')


@login_required(login_url='company:login', redirect_field_name='next')
def locations(request, slugParam):
    vehicle = Vehicle.objects.get(slug=slugParam)
    tabela = Location.objects.filter(id_company=request.user,
                                     id_vehicle=vehicle).order_by('start_location')
    number = Location.objects.filter(id_vehicle=vehicle).count()
    data = None
    tag = "Locações"
    removeTag = 'location:remove'
    editTag = "location:edit"
    portionTag = "gains:portions"
    finished = Location.objects.filter(id_vehicle=vehicle, status=False)
    try:
        if request.POST.get('inputSearch'):
            data = request.POST.get('inputSearch')

            if Location.objects.filter(id_vehicle=vehicle, start_location__icontains=data).exists():
                tabela = Location.objects.filter(id_vehicle=vehicle,
                                                 start_location__icontains=data)
            elif Location.objects.filter(id_vehicle=vehicle, end_location__icontains=data).exists():
                tabela = Location.objects.filter(id_vehicle=vehicle,
                                                 end_location__icontains=data)
            elif Location.objects.filter(id_vehicle=vehicle, id_empresa=data).exists():
                tabela = Location.objects.filter(id_vehicle=vehicle,
                                                 id_empresa=data)
            elif Location.objects.filter(id_vehicle=vehicle, total_value__icontains=data).exists():
                tabela = Location.objects.filter(id_vehicle=vehicle,
                                                 total_value__icontains=data)
            elif Location.objects.filter(id_vehicle=vehicle, number_months__icontains=data).exists():
                tabela = Location.objects.filter(id_vehicle=vehicle,
                                                 number_months__icontains=data)
            elif Location.objects.filter(id_vehicle=vehicle, id__icontains=data).exists():
                tabela = Location.objects.filter(id_vehicle=vehicle,
                                                 id__icontains=data)
            else:
                tabela = None
                data = None
    except:
        tabela = None
        data = None

    return render(request, 'location/locacoes.html', {'active': 1, 'prev': 'location:locations', 'removeTag': removeTag, 'include': 1, 'portionTag': portionTag, 'editTag': editTag, 'finished': finished, 'tag': tag, 'number': number, 'resultados': data, 'slug': slugParam, 'vehicle': vehicle,  'tabela': tabela})  # noqa


@login_required(login_url='company:login', redirect_field_name='next')
def edit(request, slugParam, id):

    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    loc = Location.objects.get(
        id_company=request.user, id_vehicle=vehicle, id=id)
    print("1: ", loc)
    print("1 Veiuclo:", vehicle)

    locationForm = LocationEditForm(instance=loc)
    pagos = Gain.objects.filter(id_location=id, it_paid=True).count()

    if pagos == 0:
        flag = True
    else:
        flag = False

    # Checar se esta na locação individual ou Geral
    if "Todos" in str(request.path):
        prev = 'location:allLocations'
        path = 'location:editAll'
        active = 2
        tag2 = True
    else:
        tag2 = False
        active = 1
        path = 'location:edit'
        prev = 'location:locations'

    anterior = locationForm['number_months'].value()
    last_date = loc.end_location
    current_date = loc.start_location

    if request.POST:

        locationForm = LocationEditForm(request.POST, instance=loc)

        if locationForm.is_valid():
            print("FORM IS VALID")
            edit = locationForm.save(commit=False)
            edit.id_vehicle = vehicle
            edit.id_company = request.user

            if pagos == 0:
                print("ENTROU NA CONDIÇÃO 0", edit.start_location)

                if Location.objects.filter(id_company=request.user, id_vehicle=vehicle, start_location__lte=edit.start_location, end_location__gte=edit.start_location).exclude(id=id).exists():  # noqa
                    messages.error(request, 'Data já existe!')
                    return redirect('location:edit', slugParam, id)

            if edit.number_months < pagos:
                messages.error(
                    request, "O numero de meses  precisa ser igual ou maior ao número de meses pagos")
            elif edit.number_months == pagos:
                edit.status = True
                edit.can_remove = False
                edit.can_edit = True
                removeGains(last_date, edit.start_location +
                            relativedelta(months=edit.number_months), edit, request.user)
                edit.save()
                return redirect('location:edit', slugParam, id)
            elif edit.number_months > pagos:

                if edit.number_months > anterior:
                    addGains(edit, request.user, pagos)
                elif edit.number_months < anterior:
                    # Adicionar Função para remover
                    removeGains(last_date, edit.start_location +
                                relativedelta(months=edit.number_months), edit, request.user)

                edit.status = True
                edit.can_edit = True
                edit.can_remove = True
                edit.save()

                messages.success(request, 'Gasto editado com sucesso')
                return redirect('location:edit', slugParam, id)

    return render(request, 'location/EditarLocacao.html', {'active': active, 'flag': flag, 'path': path, 'name': 'location', 'tag2': tag2, 'prev': prev, 'name': 'Locação', 'id': id, 'slug': slugParam, 'vehicle': vehicle, 'form': locationForm})


@login_required(login_url='company:login', redirect_field_name='next')
def gerarContrato(request, id):
    location = Location.objects.get(id_company=request.user, id=id)
    contract = Contract.objects.get(id_location=location)

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    createPdf(p, contract)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='location-'+str(location.id)+'.pdf')


@login_required(login_url='company:login', redirect_field_name='next')
def loc(request):

    vehicle = Vehicle.objects.filter(company_user=request.user)
    tabela = Location.objects.filter(
        id_company=request.user).order_by('-start_location')
    number = Location.objects.filter(id_company=request.user).count()
    data = None
    tag = "Locações"
    removeTag = 'location:removeAll'
    editTag = 'location:editAll'
    portionTag = 'gains:allPortions'
    finished = Location.objects.filter(id_company=request.user, status=False)

    if request.POST.get('inputSearch'):
        data = request.POST.get('inputSearch')
        try:
            if Location.objects.filter(id_company=request.user, start_location__icontains=data).exists():
                tabela = Location.objects.filter(id_company=request.user,
                                                 start_location__icontains=data).order_by('-start_location')
            elif Location.objects.filter(id_company=request.user, end_location__icontains=data).exists():
                tabela = Location.objects.filter(id_company=request.user,
                                                 end_location__icontains=data).order_by('-start_location')
            elif Location.objects.filter(id_company=request.user, id_empresa=data).exists():
                tabela = Location.objects.filter(id_company=request.user,
                                                 id_empresa=data).order_by('-start_location')
            elif Location.objects.filter(id_company=request.user, total_value__icontains=data).exists():
                tabela = Location.objects.filter(id_company=request.user,
                                                 total_value__icontains=data).order_by('-start_location')
            elif Location.objects.filter(id_company=request.user, number_months__icontains=data).exists():
                tabela = Location.objects.filter(id_company=request.user,
                                                 number_months__icontains=data).order_by('-start_location')
            elif Location.objects.filter(id_company=request.user, id__icontains=data).exists():
                tabela = Location.objects.filter(id_company=request.user,
                                                 id__icontains=data).order_by('-start_location')
            else:
                tabela = None
                data = None
        except:
            tabela = None
            data = None

    return render(request,  'location/locacoes.html', {'active': 2, 'include': 2, 'prev': 'location:allLocations', 'removeTag': removeTag, 'portionTag': portionTag, 'editTag': editTag, 'finished': finished, 'tag': tag, 'number': number, 'resultados': data, 'slug': None, 'vehicle': vehicle,  'tabela': tabela})


@login_required(login_url='company:login', redirect_field_name='next')
def remove(request, slugParam, id):

    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)

    remove = Location.objects.get(id_vehicle=vehicle, id=id)

    gains = Gain.objects.filter(id_location=remove, id_vehicle=vehicle, date__range=[
        remove.start_location, remove.end_location], it_paid=False)

    if gains.count() == remove.number_months:
        remove.delete()
        vehicle.it_location = False
        vehicle.save()
    else:
        remove.number_months -= gains.count()
        remove.end_location -= relativedelta(months=gains.count())
        remove.status = True
        remove.can_remove = False
        remove.can_edit = False
        remove.save()

        if datetime.date.today() >= remove.end_location:
            remove.status = False
            remove.save()
            vehicle.it_location = False
            vehicle.save()
    gains.delete()

    if "Todas" in request.path:
        return redirect('location:allLocations')
    else:
        return redirect('location:locations', slugParam)


@ login_required(login_url='company:login', redirect_field_name='next')
def locar(request, slugParam, profileParam):
    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)

    if request.POST:
        form = LocationForm(request.POST)

        if form.is_valid():
            register = form.save(commit=False)
            register.id_vehicle = vehicle
            register.id_company = request.user
            register.status = True  # em andamento e pode ser editado
            register.can_remove = True  # Pode ser removido
            register.save()
            vehicle.it_location = True
            vehicle.save()
            addGains(register, request.user, 0)
            print("REGISTER", register.start_location)
            gerarObj(register)
            messages.success(request, 'Locação Cadastrada com Sucesso')
            form = LocationForm()
        else:
            print("NAO E VALISo")

    else:
        form = LocationForm()

    return render(request, 'location/locar.html', {'active': 1, 'flag': False, 'vehicle': vehicle,  'form': form, 'profile': profileParam, 'slug': slugParam})
