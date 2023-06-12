import datetime
import io
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import exception
from multiprocessing.connection import Client

from client_Company.models import Client_company
from company.models import Company
from dateutil.relativedelta import relativedelta
from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.forms import ValidationError
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from gain.addGains import addGains, removeGains
from gain.models import Gain
from Optar.settings import BASE_DIR, STATICFILES_DIRS
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

    data = request.GET.get('inputSearch')
    if data:

        if len(data) > 0:
            if data.isdigit():
                tabela = Location.objects.filter(Q(id_company=request.user) & Q(Q(  # noqa
                    Q(total_value__icontains=data) | Q(number_months=int(data)) | Q(id__iexact=data)))).order_by('-start_location')  # noqa
            else:
                tabela = Location.objects.filter(Q(id_company=request.user) & Q(Q(start_location__icontains=data) | Q(end_location__icontains=data) | Q(  # noqa
                    empresa_name__icontains=data))).order_by('-start_location')  # noqa
            if tabela.count() == 0:
                tabela = None
                data = None

    return render(request, 'location/locacoes.html', {'active': 1, 'prev': 'location:locations', 'removeTag': removeTag, 'include': 1, 'portionTag': portionTag, 'editTag': editTag, 'finished': finished, 'tag': tag, 'number': number, 'resultados': data, 'slug': slugParam, 'vehicle': vehicle,  'tabela': tabela})  # noqa


@login_required(login_url='company:login', redirect_field_name='next')
def edit(request, slugParam, id):

    vehicle = Vehicle.objects.get(company_user=request.user, slug=slugParam)
    loc = Location.objects.get(
        id_company=request.user, id_vehicle=vehicle, id=id)

    pagos = Gain.objects.filter(id_location=id, it_paid=True).count()
    locationForm = LocationEditForm(instance=loc)

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

            edit = locationForm.save(commit=False)
            edit.id_vehicle = vehicle
            edit.id_company = request.user

            if pagos == 0:

                if Location.objects.filter(id_company=request.user, id_vehicle=vehicle, start_location__lte=edit.start_location, end_location__gte=edit.start_location).exclude(id=id).exists():  # noqa
                    messages.error(request, 'Data já existe!')
                    return redirect(path, slugParam, id)

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
                messages.success(request, 'Gasto editado com sucesso')
                return redirect(path, slugParam, id)
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
                return redirect(path, slugParam, id)

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
    info = "(formato de data yyyy-mm-dd)"

    if request.GET.get('inputSearch'):
        data = request.GET.get('inputSearch')

        if len(data) > 0:
            if data.isdigit():
                tabela = Location.objects.filter(Q(id_company=request.user) & Q(Q(  # noqa
                    Q(total_value__icontains=data) | Q(number_months=int(data)) | Q(id__iexact=data)))).order_by('-start_location')  # noqa
            else:
                tabela = Location.objects.filter(Q(id_company=request.user) & Q(Q(start_location__icontains=data) | Q(end_location__icontains=data) | Q(  # noqa
                    empresa_name__icontains=data))).order_by('-start_location')  # noqa
            if tabela.count() == 0:
                tabela = None
                data = None

    return render(request,  'location/locacoes.html', {'active': 2, 'include': 2, 'prev': 'location:allLocations', 'info': info, 'removeTag': removeTag, 'portionTag': portionTag, 'editTag': editTag, 'finished': finished, 'tag': tag, 'number': number, 'resultados': data, 'slug': None, 'vehicle': vehicle,  'tabela': tabela})


@ login_required(login_url='company:login', redirect_field_name='next')
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
    companies = Client_company.objects.filter(company_user=request.user)

    if request.POST:
        form = LocationForm(request.POST)

        if form.is_valid():
            register = form.save(commit=False)
            register.id_vehicle = vehicle
            idEmpresa = request.POST.get('empresas')
            register.id_empresa = Client_company.objects.get(id=idEmpresa)
            register.id_company = request.user
            register.slug_vehicle = vehicle.slug
            register.status = True  # em andamento e pode ser editado
            register.can_remove = True  # Pode ser removido
            register.save()
            vehicle.it_location = True
            vehicle.save()
            addGains(register, request.user, 0)
            gerarObj(register)
            messages.success(request, 'Locação Cadastrada com Sucesso')
            form = LocationForm()

    else:
        form = LocationForm()

    return render(request, 'location/locar.html', {'companies': companies, 'active': 1, 'flag': False, 'vehicle': vehicle,  'form': form, 'profile': profileParam, 'slug': slugParam})


@ login_required(login_url='company:login', redirect_field_name='next')
def enviarEmail(request, slugParam, empresa, id):
    locacao = Location.objects.get(id=id)
    contract = Contract.objects.get(id_location=locacao)

    emp = Client_company.objects.get(company_user=request.user, id=empresa)

    host = "smtp.gmail.com"
    port = '587'
    login = 'vitornt434@gmail.com'
    senha = "gzhzkyywxlzjadpj"

    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(login, senha)

    # MONTANDO EMAIL
    f = open(
        str(BASE_DIR)+"/templates/emailModel.html", 'r', encoding='utf-8')
    corpo = f.read()
    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = emp.email
    email_msg['Subject'] = "Contrato de Locação OPTAR: "+str(emp.name)
    email_msg.attach(MIMEText(corpo, 'html'))

    pdf = canvas.Canvas(str(BASE_DIR)+"/ContratoNº"+str(locacao.id)+".pdf")
    createPdf(pdf, contract)
    pdf.save()
    attachment = open(str(BASE_DIR)+"/ContratoNº" +
                      str(locacao.id)+".pdf", 'rb')

    att = MIMEBase('application', 'octet-stream')
    att.set_payload(attachment.read())
    encoders.encode_base64(att)

    att.add_header('content-Disposition',
                   f'attachment; filename= Contrato.pdf')
    attachment.close()

    email_msg.attach(att)

    # ENVIANDO EMAIL

    try:
        server.sendmail(email_msg['From'],
                        email_msg['To'], email_msg.as_string())
        server.quit()
        messages.success(request, 'email enviado com sucesso')

    except:
        messages.error(
            request, 'Nao foi possivel enviar o email, tende novamente')
    return redirect('location:allLocations')
