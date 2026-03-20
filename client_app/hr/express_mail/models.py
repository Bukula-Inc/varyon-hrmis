from django.db import models
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel

class Express_Mail (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    officer_id = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    justification_of_mail = models.TextField (default="", null=True)
    officer_name = models.CharField (max_length=255, null=True, default="")
    mail_destination = models.CharField (max_length=255, null=True, default="")
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'express_mail'
