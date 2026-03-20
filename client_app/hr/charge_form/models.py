from django.db import models
from client_app.hr.employee.models import Employee
from client_app.hr.offence.models import Offence
from client_app.hr.violation_type.models import Violation_Type
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel , TableModel
from datetime import date
# # Create your models here.

class Charge_Witness(TableModel):
    witness =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="witness")
    witness_name =models.CharField(max_length=255, default="", null=True)
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True)

    class Meta:
        db_table = 'charge_witness' 


class Charge_Form(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    employee =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="charged_officer")
    employee_name =models.CharField(max_length=255, default="", null=True)
    engagement_date =models.DateField(default=date.today, null=True)
    job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    date_of_occurrence =models.DateField(default=date.today, null=True)
    place_of_occurrence =models.CharField(max_length=255, default="", null=True)
    offence =models.ForeignKey(Offence, on_delete=models.DO_NOTHING, default=None, null=True)
    meantime =models.CharField(default="", null=True)
    facts_of_occurrence =models.TextField(max_length=255, default="", null=True)
    charging_office_id =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="charging_officer")
    charging_office_name =models.CharField(max_length=255, default="", null=True)
    charging_date =models.DateField(default=date.today, null=True)
    charge_witness =models.ManyToManyField(Charge_Witness, blank=True)
    # attachment_evidence = models.TextField(null=True, default="")
    staff_id = models.CharField(max_length=255, default="", null=True)

    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'charge_form' 



