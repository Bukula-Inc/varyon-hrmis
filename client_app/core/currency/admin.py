from django.contrib import admin
from .models import Currency, Exchange_Rate
# Register your models here.
admin.site.register(Currency)
admin.site.register(Exchange_Rate)