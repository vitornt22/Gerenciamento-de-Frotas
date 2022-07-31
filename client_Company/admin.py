from django.contrib import admin

from .models import Client_company


# Register your models here.
@admin.register(Client_company)
class Client_companyAdmin(admin.ModelAdmin):
    ...
