import datetime


def calculateNumberMonths(dateInicio, dateFim):
    diferenca = dateFim-dateInicio
    return (diferenca.days)/30
