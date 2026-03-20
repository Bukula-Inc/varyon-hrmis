from django.db import models

from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.violation_type.models import Violation_Type
from client_app.hr.employee_grievance.models import Employee_Grievance
from client_app.hr.disciplinary_committee.models import Disciplinary_Committee

from client_app.models import BaseModel
from datetime import date



class Employee_Disciplinary(BaseModel):
    name = models.CharField(unique=True, max_length=255,null=True)
    issue = models.ForeignKey (Employee_Grievance, on_delete=models.DO_NOTHING, default=None, null=True)
    issue_raiser = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    issue_raiser_name = models.CharField(max_length=255, default="",null=True)
    issue_raiser_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True)
    issue_raiser_reports_to = models.CharField(max_length=255, default="",null=True)
    subject = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="subject", default="", null=True)
    subject_name = models.CharField(max_length=255, default="",null=True)
    subject_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name="subject_department", default=None, null=True)
    subject_reports_to = models.CharField(max_length=255,  default="",null=True)
    date_of_warning= models.DateField(default=date.today,null=True)
    violation_type = models.ForeignKey(Violation_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    violation_date= models.DateField(default=date.today, null=True)
    violation_location = models.CharField(max_length=255, default="",null=True)
    description_of_violation = models.TextField(max_length=255, default="",null=True)
    subject_statement = models.TextField(max_length=255, default="", null=True)
    displinary_committee =models.ForeignKey(Disciplinary_Committee, on_delete=models.DO_NOTHING, default=None, null=True)
    violation_to_date = models.DateField(default=date.today, null=True)
    # NEWLY ADDED
    accursed_officer_report =models.TextField(default="", null=True)
    charge =models.CharField(max_length=255, default=None, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee_disciplinary' 



