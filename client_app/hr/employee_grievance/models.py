from django.db import models
from client_app.core.company.models import Company
from client_app.hr.disciplinary_committee.models import Disciplinary_Committee
from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.grievance_type.models import Grievance_Type
from client_app.hr.violation_type.models import Violation_Type

from client_app.models import BaseModel
from datetime import date



class Employee_Grievance(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    subject = models.CharField (max_length=255, default='', null=True)
    grievance_date= models.DateField(default=date.today,null=True)
    raised_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    employee_name = models.CharField(max_length=255, default="",null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True)
    reports_to = models.CharField(max_length=255, default="",null=True)
    grievance_against = models.ForeignKey(Employee, related_name="grievance_against", on_delete=models.DO_NOTHING, default=None, null=True)
    # grievance_type = models.CharField(max_length=255, default="", null=True)
    description = models.TextField(default="",null=True)
    cause_of_grievance = models.TextField( default="", null=True)
    # resolution_date = models.DateField(max_length=255, default="", null=True)
    # resolved_by = models.ForeignKey(Employee, related_name="resolved_by", on_delete=models.DO_NOTHING, default=None, null=True)
    # resolution_details = models.TextField(max_length=255, default="", null=True)
    # escalation = models.CharField (max_length=255, default='', null=True, blank=True)
    # violation_type =models.ForeignKey(Violation_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    company = models.ForeignKey (Company, on_delete=models.DO_NOTHING, default=None, null=True)
    # NEWLY ADDED
    grievance_attachment =models.TextField(default="", null=True)
    disciplinary_committee =models.ForeignKey(Disciplinary_Committee, related_name="disciplinary_committee", on_delete=models.DO_NOTHING, default=None, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)
    grievance_type =models.ForeignKey(Grievance_Type, on_delete=models.DO_NOTHING, default=None, null=True)



    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee_grievance' 
