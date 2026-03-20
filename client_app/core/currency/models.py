from django.db import models
from client_app.core.country.models import Country

from client_app.models import BaseModel, TableModel

# Create your models here.
class Currency(BaseModel):
    name = models.CharField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True, default=None)
    fraction = models.CharField(max_length=10, default='',null=True)
    symbol = models.CharField(max_length=10, null=True, default='')
    include_in_forex_table = models.IntegerField(default=0,null=True)
    include_in_quick_rates = models.IntegerField(default=0,null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'currency'
        
        
class Exchange_Rate(BaseModel):
    name = models.CharField(unique=True)
    from_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name="fxfrom_curr", null=True, default=None)
    to_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name="fxto_curr", null=True, default=None)
    rate = models.FloatField(default=0.00)
    inverse = models.FloatField(default=0.00)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'exchange_rate'

class Exchange_Rate_History(BaseModel):
    name = models.CharField(unique=True)
    from_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name="fxhfrom_curr", null=True, default=None)
    to_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name="fxhto_curr", null=True, default=None)
    rate = models.FloatField(default=0.00)
    inverse = models.FloatField(default=0.00)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'exchange_rate_history'