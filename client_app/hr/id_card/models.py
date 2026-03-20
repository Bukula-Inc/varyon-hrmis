from django.db import models

from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.core.company.models import Company
from client_app.models import BaseModel , TableModel
from datetime import date

class ID_Card(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    officer_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True)
    officer_name = models.CharField(max_length=255, default="",null=True)
    duly_appointed_as = models.IntegerField(default=0, null=True)
    salary_scale = models.CharField(max_length=255, null=True, default="")
    nrc = models.CharField(max_length=255, null=True, default="")
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None,null=True)
    job_title = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None,null=True)
    a_replacement_card_be_issued = models.IntegerField(default=0, null=True)
    reason_for_application =models.TextField(default="", null=True)
    submittion_date =models.DateField(default=date.today, null=True)
    card_cost_on_employee = models.IntegerField(default=0, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'id_card'



