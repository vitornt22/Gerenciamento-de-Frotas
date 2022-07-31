import datetime
from unittest import defaultTestLoader

from company.models import Company
from django.db import models
from django.utils.text import slugify


def year_choices():
    lista = []
    for i in range(1950, datetime.date.today().year+1):
        lista.append((i, i))
    return lista


def current_year():
    return datetime.date.today().year


YEARS = year_choices()


class Vehicle(models.Model):

    id = models.BigAutoField(primary_key=True)
    vehicle_type = models.CharField(max_length=50)
    year = models.IntegerField(choices=YEARS, default=current_year)
    company_user = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_model = models.CharField(max_length=60)
    brand = models.CharField(max_length=50)
    chassi = models.CharField(unique=True,
                              max_length=21)
    license_plate = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)
    it_location = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.vehicle_type + '-' + str(self.year) + '' + self.chassi

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.chassi)}'
            self.slug = slug
        self.chassi = self.chassi.upper()
        self.license_plate = self.license_plate.upper()

        return super().save(*args, **kwargs)


class Vehicle_Types (models.Model):

    company_user = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True)
    types = models.CharField(max_length=50)

    def __str__(self):
        return self.types + '-' + str(self.company_user)
