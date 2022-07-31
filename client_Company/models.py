from company.models import Company
from django.db import models
from django.utils.text import slugify

ESTADOS = (('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),  # noqa
           ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'),  # noqa
            ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),  # noqa
           ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'))

# Create your models here.


class Client_company (models.Model):

    id = models.BigAutoField(primary_key=True)
    cnpj = models.CharField(null=False, unique=True,
                            blank=False, max_length=18)
    state = models.CharField(
        choices=ESTADOS, max_length=2, null=False, blank=False)
    company_user = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    contact = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    adress = models.CharField(blank=False, null=False, max_length=40)
    district = models.CharField(blank=False, null=False, max_length=40)
    zip_code = models.CharField(blank=False, null=False,  max_length=9)
    number = models.CharField(max_length=100)
    city = models.CharField(null=False, blank=False, max_length=50)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name + '- ' + self.cnpj

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.cnpj)}'
            self.slug = slug

        return super().save(*args, **kwargs)
