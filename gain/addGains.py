from dateutil.relativedelta import relativedelta

from .models import Gain


def removeGains(last_date, atual_date, location, company):
    ganhos_remove = Gain.objects.filter(
        id_location=location, id_company=company, date__range=[atual_date, last_date])
    ganhos_remove.delete()


def addGains(location, company, pagos):
    date = location.start_location + relativedelta(months=pagos)

    if location.number_months > pagos:
        aux = 0
    else:
        aux = 1

    for i in range(pagos, location.number_months):
        if not Gain.objects.filter(id_location=location, id_company=company, date=date).exists():  # noqa
            newGain = Gain()
            # MUDAR PRA ID LOCACAO
            newGain.id_location = location
            newGain.id_vehicle = location.id_vehicle
            newGain.id_company = company
            newGain.occasion = "Locacao para empresa " + \
                location.id_empresa.name + ", CNPJ: " + \
                str(location.id_empresa.cnpj) + " em " + str(date) + \
                "no valor de : " + str(location.monthly_value)
            newGain.valor = location.monthly_value
            newGain.date = date
        else:
            newGain = Gain.objects.get(
                id_location=location, id_company=company, date=date)

        if aux == 0:
            newGain.can_pay = True

        aux += 1
        newGain.save()

        date = date + relativedelta(months=1)
