from django.db import models
from client_app.core.company.models import Company
from client_app.core.currency.models import Currency
from client_app.models import BaseModel, TableModel

class Share_Type(BaseModel):
    name = models.CharField(null=True, unique=True)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    price_per_share = models.FloatField(null=True, default=0.00)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'share_type'

class Shareholder(BaseModel):
    name = models.CharField(null=True, unique=True)
    first_name = models.CharField(null=True, default="")
    last_name = models.CharField(null=True, default="")
    other_names = models.CharField(null=True, default="")
    email = models.CharField(null=True, unique=True, default="")
    contact = models.CharField(null=True, unique=True, default="")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'shareholder'

class Share_Shareholder(TableModel):
    shareholder = models.ForeignKey(Shareholder, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    first_name = models.CharField(null=True, default="")
    last_name = models.CharField(null=True, default="")
    shareholder_share_percentage = models.FloatField(null=True, default=0.00)
    shareholder_total_shares = models.FloatField(null=True, default=0.00)
    shareholder_share_value = models.FloatField(null=True, default=0.00)
    class Meta:
        db_table = 'share_shareholder'

class Share(BaseModel):
    name = models.CharField(unique=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    share_type = models.ForeignKey(Share_Type, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    total_shares = models.FloatField(default=0.00, null=True)
    price_per_share = models.FloatField(default=0.00, null=True)
    total_value = models.FloatField(default=0.00, null=True)
    shareholders = models.ManyToManyField(Share_Shareholder, blank=True)
    total_shareholders = models.FloatField(default=0.00, null=True)
    total_owned_shares = models.FloatField(default=0.00, null=True)
    total_owned_value = models.FloatField(default=0.00, null=True)
    total_unowned_shares = models.FloatField(default=0.00, null=True)
    total_unowned_value = models.FloatField(default=0.00, null=True)
    class Meta:
        db_table = 'share'
