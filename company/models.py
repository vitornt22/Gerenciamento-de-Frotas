from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
ESTADOS = (('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),  # noqa
           ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'),  # noqa
            ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),  # noqa
           ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'))


class CompanyManager(BaseUserManager):
    def create_user(self, cnpj, company_name, email, password=None):
        if not cnpj:
            raise ValueError('Cnpj é necessário')
        if not company_name:
            raise ValueError('Nome da empresa é necessário')
        if not email:
            raise ValueError('Email é necessário')
        if not password:
            raise ValueError('Senha é necessária')

        user = self.model(
            cnpj=cnpj,
            company_name=company_name,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cnpj, company_name, email, password=None):
        user = self.create_user(
            cnpj=cnpj,
            company_name=company_name,
            email=email,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Company (AbstractBaseUser):
    company_name = models.CharField(
        blank=False, null=False, verbose_name='company name', max_length=80)
    email = models.EmailField(blank=False, null=False,
                              verbose_name='email adress', unique=True)
    cnpj = models.CharField(blank=False, null=False, verbose_name='cnpj', primary_key=True, max_length=18)  # noqa
    password = models.CharField(
        blank=False, null=False, verbose_name='password', max_length=88, )
    phone = models.CharField(verbose_name='phone number',
                             blank=True, null=True, max_length=15)
    adress = models.CharField(verbose_name='adress company', blank=True, null=True, max_length=50)  # noqa
    district = models.CharField(
        verbose_name='district company', blank=True, null=True, max_length=50)
    city = models.CharField(verbose_name='city company',
                            blank=False, null=False, max_length=30)
    state = models.CharField(verbose_name='uf company',  blank=True, null=True, max_length=2, choices=ESTADOS)  # noqa
    zip_code = models.CharField(
        verbose_name='zip code company',  blank=True, null=True,  max_length=9)
    is_admin = models.BooleanField(blank=True, null=True, default=False)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    is_staff = models.BooleanField(blank=True, null=True, default=False)
    is_superuser = models.BooleanField(blank=True, null=True, default=False)

    USERNAME_FIELD = 'cnpj'
    REQUIRED_FIELDS = ['company_name', 'email', 'password']

    objects = CompanyManager()

    def __str__(self):
        return self.company_name + '- ' + str(self.cnpj)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
