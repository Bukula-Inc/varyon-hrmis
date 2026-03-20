from django.db import models
from client_app.models import BaseModel 
from client_app.hr.employee.models import Employee
from client_app.hr.training_event.models import Training_Event
from client_app.hr.training_program_type.models import Training_Program_Type

class Training_Program_Application(BaseModel):
    name = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True)
    first_name = models.CharField(max_length=255,  null=True, default="")
    last_name = models.CharField(max_length=255,  null=True, default="")
    gender = models.CharField(max_length=255,  null=True, default="")
    email = models.EmailField(max_length=255,  null=True, default="")
    training_program = models.ForeignKey(Training_Program_Type, on_delete=models.DO_NOTHING,  null=True, default="")
    company = models.CharField(max_length=255,  null=True, default="")
    department = models.CharField(max_length=255, null=True, default="")
    level = models.CharField(max_length=255,  null=True, default="")
    course = models.CharField(max_length=255,  null=True, default="")
    staff_id =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="training_program_application_staff_id")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "training_program_application"
