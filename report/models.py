from company.models import Company
from django.db import models

# Create your models here.


class Report(models.Model):

    id = models.BigAutoField(primary_key=True)
    id_company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
