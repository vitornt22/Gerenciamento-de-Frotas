from django.contrib import admin

from .models import Gain


# Register your models here.
@admin.register(Gain)
class GainAdmin(admin.ModelAdmin):
    ...
