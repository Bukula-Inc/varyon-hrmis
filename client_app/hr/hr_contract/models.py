from django.db import models
from django.utils import timezone
from client_app.models import BaseModel
from client_app.hr.employment_type.models import Employment_Type
from client_app.hr.employee.models import Employee
from client_app.core.company.models import Company

class Hr_Contract (BaseModel):
    name = models.CharField (max_length=255, unique=True, default="", null=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    full_name = models.CharField (max_length=255, null=True, default="")
    company = models.ForeignKey (Company, on_delete=models.DO_NOTHING, default=None, null=True)
    period = models.IntegerField (default=0, null=True)
    previous_processed = models.IntegerField (default=0, null=True)
    contract_type = models.ForeignKey (Employment_Type, models.DO_NOTHING, default=None, null=True)
    effective_date = models.DateField (default=timezone.now, null=True)
    last_pp_date = models.DateField (default=timezone.now, null=True)
    end_date = models.DateField (default=timezone.now, null=True)
    contract_content = models.TextField (blank=True, null=True)
    basic_salary = models.FloatField (default=0.00, blank=True, null=True)

    class Meta:
        db_table = "hr_contract"

    def __str__(self) -> str:
        return self.name