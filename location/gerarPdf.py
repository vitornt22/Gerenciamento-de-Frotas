import datetime
import os
from cmath import rect

from company.models import Company
from Optar.settings import STATICFILES_DIRS
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from .models import Contract


def gerarObj(location):
    v = location.id_vehicle
    e = location.id_company
    print("VALOR DE E: ")
    client = location.id_empresa
    try:
        contract = Contract.objects.get(id_location=location)
    except:
        contract = Contract()

    contract.name = e.company_name
    contract.cnpj = e.cnpj
    contract.id_location = location
    contract.adress = ""+e.adress+','+e.district + \
        ',' + e.city+'-'+e.state+' '+e.zip_code
    contract.phone = e.phone
    contract.year = v.year
    contract.description = v.vehicle_type+" " + v.vehicle_model
    contract.chassi = v.chassi
    contract.license_plate = v.license_plate
    contract.client_name = client.name
    contract.client_adress = ""+client.adress+', '+client.district + \
        ', ' + client.city+'-'+client.state+' '+client.zip_code
    contract.client_city = client.city
    contract.client_email = client.email
    contract.client_cnpj = client.cnpj
    contract.client_phone = client.contact
    contract.client_state = client.state
    contract.save()


def table(pdf, cont, cont2, lista1, lista2, size):
    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    for i in range(size):
        pdf.rect(20, cont, 350, 20, stroke=1, fill=0)

        pdf.drawString(23, cont2, lista1[i])

        pdf.rect(370, cont, 200, 20, stroke=1, fill=0)

        pdf.drawString(378, cont2, lista2[i])

        cont -= 20
        cont2 -= 20
    return cont


def createPdf(pdf, c):

    # CREATEHEADER
    img = STATICFILES_DIRS[0] + '/dist/img/logoBranco.jpg'
    pdf.setStrokeColor(colors.black)
    pdf.rect(10, 700, 575, 60, stroke=1)
    pdf.drawImage(img, 20, 705, 110, 50)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(150, 725, "RECIBO DE LOCAÇÃO" + str(datetime.date.today())+"        Nº: " +
                   str(c.id_location.id))

    pdf.rect(10, 180, 575, 500, stroke=1)
    pdf.setFont("Helvetica-Bold", 15)
    # tables
    pdf.setStrokeColor(colors.black)
    pdf.setFillColor('#190075')
    pdf.rect(20, 630, 550, 20, stroke=1, fill=1)
    pdf.setFillColor('#ffffff')
    pdf.drawString(200, 635, "EMPRESA LOCADORA")

    lista1 = ["Empresa Locadora: " + c.name,  "Endereço: "+c.adress,
              "Modelo: "+c.description, "CHASSI: "+c.chassi]
    lista2 = ["CNPJ: "+str(c.cnpj), "Contato: "+str(c.phone),
              "Placa: "+c.license_plate, "Ano: "+str(c.year)]
    cont = 610
    cont2 = 615
    cont = table(pdf, cont, cont2, lista1, lista2, 4)

    # tabela2
    lista1 = ["Estação de Retirada: "+c.name,
              "Estação de Devolução: "+c.name]
    lista2 = ["Valor Total: "+str(c.id_location.total_value), "Nº de Meses: "+str(c.id_location.number_months),
              "Data Final: "+str(c.id_location.end_location), "Data de Inicio: "+str(c.id_location.start_location)]

    cont -= 50
    aux = 0
    for i in range(2):
        pdf.rect(20, cont, 350, 40, stroke=1, fill=0)
        pdf.drawString(23, cont+20, lista1[i])
        cont -= 40

    aux = cont
    for i in range(4):
        pdf.rect(370, aux+40, 200, 20, stroke=1, fill=0)
        pdf.drawString(373, aux+50, lista2[i])
        aux += 20

    # Table3
    if c.id_location.status == True:
        a = 'em andamento'
    else:
        a = 'findada'
    pdf.setStrokeColor(colors.black)
    pdf.setFillColor('#190075')
    pdf.rect(20, cont, 550, 20, stroke=1, fill=1)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.setFillColor('#ffffff')
    pdf.drawString(200, cont+5, "EMPRESA CLIENTE")

    lista1 = ["Nome: "+c.client_name,
              "Endereço "+c.client_adress, "Email: "+c.client_email, "Cidade: "+c.client_city]  # noqa
    lista2 = ["CNPJ: "+c.client_cnpj, "Contato: " +
              c.client_phone, "Estado: "+c.client_state, "Locação: "+a]

    cont -= 20
    cont2 = cont+5
    cont = table(pdf, cont, cont2, lista1, lista2, 4) - 40

    # Total Value
    pdf.setFont('Helvetica-Bold', 10)
    pdf.rect(150, cont, 250, 20, stroke=1, fill=0)
    pdf.drawString(153, cont+7, "Valor Total: (R$) " +
                   str(c.id_location.total_value))

    # SAVE PDF
    return pdf
