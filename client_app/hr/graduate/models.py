from django.db import models
from client_app.models import BaseModel
from client_app.hr.hr_contract.models import Hr_Contract

class Gratuity (BaseModel):
    name = models.CharField (max_length=255, unique=True, default="", null=True)
    employee = models.CharField (max_length=255, default="", null=True)
    employee_name = models.CharField (max_length=255, default="", null=True)
    basic_salary = models.FloatField (default=0.00, blank=True, null=True)
    effective_date = models.CharField (max_length=255, default="", null=True)
    gratuity_period = models.CharField (max_length=255, default="", null=True)
    expiry_contract_date = models.CharField (max_length=255, default="", null=True)
    effective_date_c = models.CharField (max_length=255, default="", null=True)
    expiry_contract_date_c = models.CharField (max_length=255, default="", null=True)
    contract_type =  models.CharField (max_length=255, default="", null=True)
    contract = models.ForeignKey (Hr_Contract, on_delete=models.DO_NOTHING, null=True, default=None)
    gratuity_amount = models.FloatField (default=0.00, blank=True, null=True)


    class Meta:
        db_table = "gratuity"

    def __str__(self) -> str:
        return self.name