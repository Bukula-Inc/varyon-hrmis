from django.db import models
from client_app.core.currency.models import Currency
from client_app.core.department.models import Department
from client_app.models import BaseModel
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Employee
from datetime import date

# Create your models here.


class ECZ_Petty_Cash(BaseModel):
    name =models.CharField(max_length=255, unique=True, null=True, default="")
    initiator =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    full_name =models.CharField(max_length=255, default="", null=True)
    designation =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    request_date =models.DateField(default=date.today, null=True)
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    requested_amount =models.FloatField(default=0.00, null=True)
    requested_amount_in_word =models.CharField(max_length=255, default="", null=True)
    purpose =models.TextField(default="", null=True)
    attachments =models.TextField(default="", null=True)
    approved_amount =models.FloatField(default=0.00, null=True)
    reporting_currency =models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=None, null=True) 

    def __str__(self):
        return self.name
    class Meta:
        db_table ="ecz_petty_cash"