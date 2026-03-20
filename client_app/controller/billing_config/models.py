from django.db import models
from client_app.core.currency.models import Currency
from client_app.models import BaseModel
from client_app.stock.items.models import Stock_Item
class Billing_Config(BaseModel):
    name = models.CharField(unique=True)
    allow_multi_select = models.IntegerField(default=0, null=True)
    trial_period = models.IntegerField(default=0, null=True)
    billing_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=None, null=True)
    annual_discount = models.FloatField(default=0.00, null=True)
    monthly_discount = models.FloatField(default=0.00, null=True)
    total_free_users = models.FloatField(default=0.00, null=True)
    cost_per_additional_user = models.FloatField(default=0.00, null=True)
    total_free_storage = models.FloatField(default=0.00, null=True)
    cost_per_additional_storage = models.FloatField(default=0.00, null=True)
    additional_storage_item = models.ForeignKey(Stock_Item, on_delete=models.DO_NOTHING, related_name="asi", null=True, default=None)
    additional_user_item = models.ForeignKey(Stock_Item, on_delete=models.DO_NOTHING, related_name="aui", null=True, default=None)
    domain_ext = models.CharField(max_length=255, null=True, default="")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'billing_config'