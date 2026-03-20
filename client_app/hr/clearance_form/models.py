from django.db import models
from client_app.hr.employee.models import Employee
from client_app.core.company.models import Company
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.hr.employee_separation.models import Employee_Seperation
from client_app.payroll.employee_grade.models import Employee_Grade
from client_app.payroll.salary_component.models import Salary_Component
from client_app.models import BaseModel , TableModel
from datetime import date
# Create your models here.

class Clearance_Form_Items(TableModel):
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True)
    item =models.CharField(max_length=255, default="", null=True)
    item_discrition =models.TextField(default="", null=True)
    hand_in_status =models.CharField(max_length=255, default="", null=True)
    hand_in_date =models.DateField(default=date.today, null=True)
    remark =models.TextField(default="", null=True)
    receiving_officer =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="receiving_officer")

    class Meta:
        db_table = 'clearance_form_items' 


class Clearance_Form(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    employee =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="leaving_officer")
    employee_name =models.CharField(max_length=255, default="", null=True)
    engagement_date =models.DateField(default=date.today, null=True)
    job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    date_of_separation =models.DateField(default=date.today, null=True)
    salary_grade =models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
    clearance_data =models.ManyToManyField(Clearance_Form_Items, blank=True)
    employee_separation =models.ForeignKey(Employee_Seperation, on_delete=models.DO_NOTHING, default=None, null=True)
    attach =models.TextField(default="", null=True)
    handover_note =models.TextField(default="", null=True)
    cleared =models.IntegerField(default=0, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

   
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'clearance_form' 



