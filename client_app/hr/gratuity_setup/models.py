from django.db import models
from client_app.core.currency.models import Currency
from client_app.models import BaseModel

class Gratuity_Configuration(BaseModel):
    name = models.CharField(max_length=255, unique=True, default="", null=True)
    gratuity_rate = models.FloatField (default=0.00, blank=True, null=True)
    # debit_account = models.ForeignKey (Account, on_delete=models.DO_NOTHING, related_name="debit_account_gratuity", null=True, default=None)
    # credit_account = models.ForeignKey (Account, on_delete=models.DO_NOTHING, related_name="credit_account_gratuity", null=True, default=None)
    transaction_currency =models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=None, null=True)
    minimum_rate = models.FloatField (default=.00, null=True)
    def __str__(self) -> str:
        return self.name
    class Meta:
        db_table = 'gratuity_configuration'