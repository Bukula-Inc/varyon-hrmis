from django.db import models
from client_app.core.company.models import Company
from client_app.core.cost_center.models import Cost_Center
from client_app.core.country.models import Country
from client_app.core.currency.models import Currency

from client_app.models import BaseModel

# Create your models here.
class System_Settings (BaseModel):
    name = models.CharField(unique=True, default='System Settings', null=True)
    default_company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, related_name='%(class)s_company', default=None)
    default_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name='%(class)s_currency', default=None)
    default_cost_center = models.ForeignKey(Cost_Center, on_delete=models.DO_NOTHING, default=None)
    default_country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, default=None)
    currency_decimals = models.IntegerField(default=2, null=True)
    api_key = models.CharField(max_length=255, null=True, default="")

    class Meta:
        db_table = 'system_settings'
        unique_together = ("name",)