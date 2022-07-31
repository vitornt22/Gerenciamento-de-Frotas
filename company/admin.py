from django.contrib import admin

from .forms import CompanyFormAdmin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    form = CompanyFormAdmin

    class Media:
        js = (
            "js/jquery.mask.min.js",
            "js/custom.js",
        )


# Register your models here.
admin.site.register(Company, CompanyAdmin)
