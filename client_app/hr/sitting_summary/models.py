from datetime import date
from django.db import models

# Create your models here.
from client_app.hr.charge_form.models import Charge_Form
from client_app.hr.employee.models import Employee
from client_app.hr.employee_grievance.models import Employee_Grievance
from client_app.hr.sanction_type.models import Sanction_Type
from client_app.models import BaseModel, TableModel

def empty_list():
    return list

class Previous_Sitting(TableModel):
    sitting =models.CharField(max_length=255, default="", null=True)
    accused_present =models.IntegerField(default=0, null=True)

    class Meta:
       db_table ="previous_sitting"


class Internal_Sitting_Attendance(TableModel):
                    
    employee =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    attendee =models.CharField(max_length=255, default="", null=True)
    attendee_email =models.CharField(max_length=255, default="", null=True)
       

    class Meta:
            db_table ="sitting_attendance"

                

class Sitting_Summary(BaseModel):

    name =models.CharField(max_length=255, unique=True, default="", null=True)
    charge =models.ForeignKey(Charge_Form, on_delete=models.DO_NOTHING, default=None, null=True)
    sitting_date =models.DateField(default=date.today, null=True)
    first_sitting =models.IntegerField(default=1, null=True)
    case_finding =models.CharField(max_length=255,default="", null=True)
    disciplinary_action =models.ForeignKey(Sanction_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    previous_sitting =models.ManyToManyField(Previous_Sitting, blank=True)
    description =models.TextField(default="", null=True)
    internal_sitting_attendance =models.ManyToManyField(Internal_Sitting_Attendance,blank=True)
    sitting_type =models.CharField(max_length=255, default="", null=True)
    next_sitting_date =models.DateField(default=date.today, null=True)
    adjournment =models.IntegerField(default=0, null=True)
    external_sitting_attendance =models.JSONField(default=empty_list(), null=True)
    grievance =models.ForeignKey(Employee_Grievance, on_delete=models.DO_NOTHING, default=None, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="sitting_summary"