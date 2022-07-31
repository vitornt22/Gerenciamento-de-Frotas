from company.models import Company
from django.db import models
from vehicle.models import Vehicle


# Create your models here.
class Spent (models.Model):
    id = models.BigAutoField(primary_key=True)
    id_company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True)
    id_vehicle = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, blank=True, null=True)
    occasion = models.TextField(blank=False, null=False)
    valor = models.FloatField(blank=False, null=False)
    date = models.DateField()

    def __str__(self):
        return "GASTO: " + str(self.id) + '-' + str(self.occasion)+'-' + str(self.date)  # noqa
