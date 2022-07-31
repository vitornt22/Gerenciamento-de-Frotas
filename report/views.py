import datetime
import io

from client_Company.models import Client_company
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from gain.models import Gain
from location.models import Location
from reportlab.pdfgen import canvas
from spent.models import Spent
from vehicle.models import Vehicle

from .gerarRelatorio import createPdf
from .models import Report

# Create your views here.


def caixa(request):
    entradas = Gain.objects.filter(id_company=request.user, it_paid=True)
    saidas = Spent.objects.filter(id_company=request.user)
    entrada = 0
    saida = 0
    for i in entradas:
        entrada += i.valor
    for i in saidas:
        saida += i.valor

    return entrada-saida


def listaFinancas(empresa):
    print("EMPRESSSA", empresa)
    entradas = [0]*12
    saidas = [0]*12
    lucro = [0]*12
    anoAtual = datetime.date.today().year
    mes = datetime.date.today().month
    for i in range(12):
        for j in Gain.objects.filter(it_paid=True, id_company=empresa, date__year=anoAtual, date__month=i+1):
            entradas[i] += j.valor
        for q in Spent.objects.filter(id_company=empresa, date__year=anoAtual, date__month=i+1):
            saidas[i] += q.valor
        lucro[i] = entradas[i]-saidas[i]
    if lucro[mes-2] == 0:
        aumento = lucro[mes-1]*100
    else:
        aumento = ((lucro[mes-1]-lucro[mes-2]) * 100) / lucro[mes-2]

    return lucro, aumento, entradas[mes-1], saidas[mes-1]


@ login_required(login_url='company:login', redirect_field_name='next')
def reports(request):
    mes = datetime.date.today().month
    lucroLista, aumento, entradas, saidas = listaFinancas(request.user)
    print("ENTRADAS: ", entradas)
    print('Saidas:', saidas)
    caixaEmpresa = caixa(request)
    qnt_company = Client_company.objects.filter(
        company_user=request.user).count()
    locations = Location.objects.filter(id_company=request.user).count
    qnt = Vehicle.objects.filter(company_user=request.user).count()
    tabela = Report.objects.filter(id_company=request.user)
    lista = []
    current_year = datetime.date.today().year
    scroll = 0
    resultados = None

    if request.POST:
        scroll = 10
        month = request.POST.get('month')
        year = str(request.POST.get('year'))
        print("ANOOO e mês ", month)
        aux = str(month)
        if len(month) > 0:
            if int(month) < 10:
                aux = '0'+str(month)
        resultados = aux+'/'+str(year)

        try:
            if Report.objects.filter(id_company=request.user, year=year, month=month).exists():
                tabela = Report.objects.filter(
                    id_company=request.user, year=year, month=month).order_by('month', 'year')
            elif len(month) == 0:
                resultados = None
            else:
                tabela = None
                resultados = None
        except:
            tabela = None
            resultados = None

    for i in range(2021, current_year+1):
        lista.append(i)

    return render(request, 'reports.html', {'caixa': caixaEmpresa, 'grafico': [entradas, saidas], 'aumento': aumento, 'lucroMes': lucroLista[int(mes)-1], 'lucroLista': lucroLista, 'qnt_company': qnt_company, 'resultados': resultados, 'scroll': scroll, 'qnt_locations': locations, 'qnt_vehicle': qnt, 'active': 3, 'anos': lista, 'tabela': tabela, })


@ login_required(login_url='company:login', redirect_field_name='next')
def gerarRelatorioView(request, id):
    report = Report.objects.get(id=id, id_company=request.user)
    print("REPOOOORT:", report)
    gains = Gain.objects.filter(it_paid=True, id_company=request.user, date__month=report.month, date__year=report.year)  # noqa
    spents = Spent.objects.filter(id_company=request.user, date__month=report.month, date__year=report.year)  # noqa
    print("GANHOS E GASTOS", gains, spents)
    print("REPOOOOSOSOSSSNSNNS: ", report)
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    createPdf(p, gains, spents, report)
    # p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='location-'+str(report.id)+'.pdf')
