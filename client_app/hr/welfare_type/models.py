from django.db import models
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel, TableModel 

# Create your models here.


class Welfare_Applicable_Department(TableModel):
    department_applicable_to =models.ForeignKey(Department, default=None, null=True, on_delete=models.DO_NOTHING)
    class Meta:
        db_table ="welfare_applicable_department"
class Welfare_Applicable_Designation(TableModel):
    designation_applicable_to =models.ForeignKey(Designation, default=None, null=True, on_delete=models.DO_NOTHING)
    class Meta:
        db_table ="welfare_applicable_designation"


class Welfare_Type(BaseModel):
    name =models.CharField(max_length=255, default="", null=True, unique=True)
    employee_privilege =models.CharField(max_length=255, default="", null=True)
    limit_unit =models.CharField(max_length=255, default="", null=True)
    limit_qty =models.IntegerField(default=0, null=True)
    company_percentage =models.FloatField(default=0.00, null=True)
    employee_percentage =models.FloatField(default=0.00, null=True)

    applicable_to_all_departments =models.IntegerField(default=0, null=True)
    applicable_to_all_designation =models.IntegerField(default=0, null=True)

    departments_applicable_to =models.ManyToManyField(Welfare_Applicable_Department, blank=True)
    designations_applicable_to =models.ManyToManyField(Welfare_Applicable_Designation, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table ="welfare_type"
