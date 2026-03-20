from django.db import models
from client_app.authentication.models import Lite_User
from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.violation_type.models import Violation_Type
from client_app.hr.employee_disciplinary.models import Employee_Disciplinary

from client_app.models import BaseModel
from datetime import date





class Case_Outcome(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    employee_disciplinary = models.ForeignKey(Employee_Disciplinary, on_delete=models.DO_NOTHING, default=None, null=True)
    subject = models.ForeignKey(Employee, on_delete=models.DO_NOTHING,  default=None, null=True)
    subject_name = models.CharField(max_length=255, default="", null=True)
    subject_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True)
    subject_reports_to = models.CharField(max_length=255,  default="",null=True)
    date_of_warning= models.DateField(default=date.today, null=True)
    violation_type = models.ForeignKey(Violation_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    violation_date= models.DateField(default=date.today, null=True)
    violation_location = models.CharField(max_length=255, default="",null=True)
    verbal_warning = models.CharField(max_length=255, default="",null=True)
    written_warning = models.CharField(max_length=255, default="",null=True)
    warning =models.TextField(default="", null=True)
    suspension= models.CharField(max_length=255, default="",null=True)
    start_date = models.DateField(default=date.today, null=True)
    end_date = models.DateField(default=date.today, null=True)
    termination = models.CharField(max_length=255, default="",null=True)
    effective_date = models.DateField(default=date.today, null=True)
 
    
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'case_outcome' 




        #     return None