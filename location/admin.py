from django.contrib import admin

from .models import Contract, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    ...


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    ...
