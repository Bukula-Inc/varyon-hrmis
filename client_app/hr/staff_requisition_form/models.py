from datetime import date
from django.db import models

# Create your models here.
from client_app.hr.contract_type.models import Hr_Contract_Type
from client_app.hr.employment_type.models import Employment_Type
from client_app.payroll.employee_grade.models import Employee_Grade
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel

class Staff_Requisition(BaseModel):
    name =models.CharField(max_length=255, default="", null=True)
    section =models.CharField(max_length=255, default="", null=True)
    employee_name =models.CharField(max_length=255, default="", null=True)
    addition_to_establishment =models.CharField(max_length=255, default="", null=True)
    source_of_recruitment =models.CharField(max_length=255, default="", null=True)
    academic =models.CharField(max_length=255, default="", null=True)
    professional =models.CharField(max_length=255, default="", null=True)
    experience =models.CharField(max_length=255, default="", null=True)
    professional_membership =models.CharField(max_length=255, default="", null=True)

    requisitioned_by =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="staff_requisition_requisitioned_by")
    requisitioners_job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True, default=None, related_name="staff_requisition_requisitioners_job_title")
    staffing_department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, default=None, related_name="staff_requisition_department")
    staffing_job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True, default=None, related_name="staff_requisition_staffing_job_title")
    employee_grade =models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, null=True, default=None, related_name="staff_requisition_staff_grade")
    contract_type =models.ForeignKey(Employment_Type, on_delete=models.DO_NOTHING, null=True, default=None, related_name="staff_requisition_hr_contract_type")
    employee_no =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="staff_requisistion_employee_being_replaced")
    
    number_required =models.IntegerField(default=0, null=True)
    is_for_replacement =models.IntegerField(default=0, null=True)
    approved_establishment =models.IntegerField(default=0.00, null=True)
    actual =models.IntegerField(default=0.00, null=True)
    variance =models.IntegerField(default=0.00, null=True)

    attach_role_profile =models.TextField(default="", null=True)

    date_required =models.DateField(default=date.today, null=True)

    available_budget =models.FloatField(default=0.00, null=True)
    budget_needed =models.FloatField(default=0.00, null=True)
    employment_type =models.ForeignKey(Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    staff_id =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="staff_requisition_requisitioner_staff_id")


    def __str__(self):
        return self.name

    class Meta:
        db_table ="staff_requisition"