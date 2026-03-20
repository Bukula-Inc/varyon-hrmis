from django.contrib import admin

from client_app.payroll.income_tax_band.models import Income_Tax_Band, Taxable_Salary_Band

# Register your models here.
admin.site.register(Income_Tax_Band)
admin.site.register(Taxable_Salary_Band)