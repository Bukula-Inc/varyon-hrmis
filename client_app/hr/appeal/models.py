from django.db import models

# Create your models here.
from client_app.hr.charge_form.models import Charge_Form
from client_app.hr.employee_grievance.models import Employee_Grievance
from client_app.models import BaseModel


class Appeal(BaseModel):
    name =models.CharField(max_length=255, unique=True, default="", null=True)
    for_type =models.CharField(max_length=255, default="", null=True)
    charge =models.ForeignKey(Charge_Form, on_delete=models.DO_NOTHING, null=True)
    grievance =models.ForeignKey(Employee_Grievance, on_delete=models.DO_NOTHING, null=True)
    supporting_document =models.TextField(null=True, default="")
    description =models.TextField(default="", null=True)

    def __self__(self):
        return self.name
    
    class Meta:
        db_table ="appeal"