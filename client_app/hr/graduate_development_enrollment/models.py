from django.db import models
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Department, Employee
from client_app.hr.employment_type.models import Employment_Type
from client_app.models import BaseModel
from client_app.payroll.employee_grade.models import Employee_Grade
from datetime import date
# Create your models here.

class Graduate_Development_Enrollment(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    requisitioned_by_full_name = models.CharField (max_length=255, null=True)
    requisitioned_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="requisitioner")
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    position = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True)
    section = models.CharField(max_length=255, null=True, default="")
    number_required = models.IntegerField(null=True, default=0)
    grade = models.IntegerField(null=True, default=0)
    employee_grade =models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, null=True, default=None)
    date_required = models.DateField(null=True, default=date.today)
    duration_of_programme = models.CharField (max_length=255, default="", null=True)
    budget = models.FloatField(null=True, default=0.00)
    attach_role_profile = models.TextField (blank=True, null=True, default="")
    attach_rotation_plan_and_areas_of_gd = models.TextField (blank=True, null=True, default="")
    supervisor = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="graduate_development_enrollment_suporviser")
    advertisement =models.CharField(default=0, null=True)
    university_or_college = models.CharField (default=0, null=True)
    # employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    academic =models.CharField(max_length=255, default="", null=True)
    professional =models.CharField(max_length=255, default="", null=True)
    supervisor_fullname = models.CharField(max_length=255, null=True, default="")
    # NEW FIELDS
    payment_method =models.CharField(max_length=255, default="", null=True)
    # source_of_enrollment =models.CharField(max_length=255, default="", null=True)

    available_budget =models.FloatField(default=0.00, null=True)
    budget_needed =models.FloatField(default=0.00, null=True)
    employment_type =models.ForeignKey(Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)



    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'graduate_development_enrollment' 
        