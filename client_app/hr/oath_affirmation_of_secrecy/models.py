from django.db import models

from client_app.hr.employee.models import Employee
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel 
from datetime import date

class Oath_Affirmation(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    empolyee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True, related_name="oath_affirmation_empolyee_id")
    employee_name = models.CharField(max_length=255, default="",null=True)
    job_title =models.CharField(max_length=255, default="", null=True)
    new_position = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None,null=True)
    sworn_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True, related_name="oath_affirmation_sworn_by")
    sworn_in_time = models.CharField(max_length=255, null=True, default="")
    declarer_name = models.CharField(max_length=255, null=True, default="")
    date_of_sworn_in = models.CharField(max_length=255, null=True, default="")
    month_of_sworn_in = models.CharField(max_length=255, null=True, default="")
    year_of_sworn_in = models.CharField(max_length=255, null=True, default="")
    sworn_in_date =models.DateField(default=date.today, null=True)
    witness_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True, related_name="oath_affirmation_witness_id")
    sworn_in_day = models.CharField(max_length=255, null=True, default="")
    witness_name = models.CharField(max_length=255, null=True, default="")    
    staff_id = models.CharField(max_length=255, default="", null=True)



    def __str__(self):
        return self.name
    class Meta:
        db_table = 'oath_affirmation'



