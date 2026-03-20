from django.db import models
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel
from client_app.payroll.employee_grade.models import Employee_Grade, Salary_Component


# Create your models here.
def default_table_data():
    return list

class Acting_Appointment(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")
    position_owner = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_position_owner")
    acting_officer = models.ForeignKey(Employee, null=True, on_delete=models.DO_NOTHING, default=None, related_name="acting_appointment_acting_person")
    start_date = models.CharField(max_length=255, null=True, default=None)
    end_date = models.CharField(max_length=255, null=True, default=None)
    acting_period = models.CharField(max_length=255, null=True, default="")
    holders_location =models.CharField(max_length=255, default="", null=True)
    daily_pay =models.FloatField(default=0.0, null=True)
    difference_payment =models.FloatField(default=0.0, null=True)
    acting_payment =models.FloatField(default=0.0, null=True)
    payable = models.IntegerField(default=0, null=True)

    # Owner's Details
    job_title = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_owners_job_title")
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_owners_department")
    salary_grade = models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_owner_salary_grade")
    salary_components =models.JSONField(default=list, null=True,)
    reason = models.TextField(null=True, default="")
    owner_name =models.CharField(max_length=255, default="", null=True)
    basic_pay =models.FloatField(default=0.0, null=True)
    holders_gross =models.FloatField(default=0.0, null=True)

    # Actor's Details
    acting_officer_job_title = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_acting_officer_job_title")
    acting_officer_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_acting_officer_department")
    acting_officer_salary_grade = models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_acting_acting_officer_salary_grade")
    acting_officer_salary_components =models.JSONField(default=list, null=True,)
    acting_officer_name =models.CharField(max_length=255, default="", null=True)
    acting_officer_basic_pay =models.FloatField(default=0.0, null=True)
    actors_gross =models.FloatField(default=0.0, null=True)

    def __str__(self):
        return f" {self.name}"
    
    class Meta:
        db_table = 'acting_appointment'

class Acting_Appointment_Memo(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")
    position_owner = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_memo_position_owner")
    acting_officer = models.ForeignKey(Employee, null=True, on_delete=models.DO_NOTHING, default=None, related_name="acting_appointment_memo_acting_person")
    start_date = models.CharField(max_length=255, null=True, default=None)
    end_date = models.CharField(max_length=255, null=True, default=None)
    acting_period = models.CharField(max_length=255, null=True, default="")
    reason = models.TextField(null=True, default="")
    acting_officer_name =models.CharField(max_length=255, default="", null=True)
    position_owner_name =models.CharField(max_length=255, default="", null=True)
    salary_grade = models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_memo_owner_salary_grade")
    job_title = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_memo_owners_job_title")
    holders_location =models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return f" {self.name}"
    
    class Meta:
        db_table = 'acting_appointment_memo'

class Acting_Appointment_Special_Grades(TableModel):
    employee_grade =models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_setup_salary_grade")
    within_country =models.FloatField(default=0.0, null=True)
    out_side_country =models.FloatField(default=0.0, null=True)

    class Meta:
        db_table ="acting_appointment_special_grades"

class Acting_Appointment_Grade_Exception(TableModel):
    employee_grade =models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, null=True, default=None, related_name="acting_appointment_setup_grade_exception")
    within_country =models.FloatField(default=0.0, null=True)
    out_side_country =models.FloatField(default=0.0, null=True)

    class Meta:
        db_table ="acting_appointment_grade_exception"

class Acting_Appointment_Settings(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")

    maturity_period = models.IntegerField(null=True, default=0)
    grade_exceptions = models.ManyToManyField(Acting_Appointment_Grade_Exception, blank=True,)
    acting_pay =models.FloatField(default=0.00, null=True)
    matured =models.IntegerField(default=0, null=True)

    position_holder_in_country =models.IntegerField(default=0, null=True)
    position_holder_outside_country =models.IntegerField(default=0, null=True)

    def __str__(self):
        return f" {self.name}"
    
    class Meta:
        db_table = 'acting_appointment_settings'