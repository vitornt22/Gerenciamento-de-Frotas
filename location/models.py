

from client_Company.models import Client_company
from company.models import Company
from dateutil.relativedelta import relativedelta
from django.db import models
from django.urls import reverse
from Optar import settings
from vehicle.models import Vehicle

# Create your models here


class Location(models.Model):

    id = models.BigAutoField(primary_key=True)
    id_company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True)
    id_vehicle = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    start_location = models.DateField(null=False, blank=False)
    number_months = models.IntegerField(blank=False, null=False)

    end_location = models.DateField(null=True, blank=True)
    empresa_name = models.CharField(null=True, blank=True, max_length=100)
    monthly_value = models.FloatField(null=False, blank=False)
    id_empresa = models.ForeignKey(
        Client_company, null=True, blank=False, on_delete=models.SET_NULL)
    total_value = models.FloatField(blank=True, null=True)
    status = models.BooleanField(default=True)
    can_remove = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.end_location = self.start_location + relativedelta(months=self.number_months)  # noqa
        self.total_value = self.monthly_value * self.number_months
        self.empresa_name = self.id_empresa.name + \
            " - "+str(self.id_empresa.cnpj)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.empresa_name + ' de ' + str(self.start_location)+" à " + str(self.end_location)


class Contract(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=50)
    id_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=17)
    year = models.CharField(max_length=4)
    description = models.CharField(max_length=50)  # model + type
    chassi = models.CharField(max_length=21)
    license_plate = models.CharField(max_length=8)
    client_name = models.CharField(max_length=50)
    client_email = models.CharField(max_length=50)
    client_adress = models.CharField(max_length=255)
    client_city = models.CharField(max_length=50)
    client_cnpj = models.CharField(max_length=50)
    client_phone = models.CharField(max_length=50)
    client_state = models.CharField(max_length=2)
