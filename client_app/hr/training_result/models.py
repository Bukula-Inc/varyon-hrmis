from django.db import models


from client_app.models import BaseModel, TableModel
from client_app.hr.training_event.models import Training_Event
from client_app.hr.employee.models import Employee


class Result(TableModel):
    training_event = models.ForeignKey( Training_Event, on_delete=models.DO_NOTHING, default=None,null=True)
    employee = models.ForeignKey( Employee, on_delete=models.DO_NOTHING, default=None,null=True)
    hours = models.CharField(max_length=255,default="",null=True)
    grade = models.CharField(max_length=255,default="",null=True)
    comment = models.CharField(max_length=255,default="",null=True)

    def __str__(self):
        return f" {self.training_event}"
    class Meta:
        db_table = 'result'

class Training_Result(BaseModel):
    name = models.CharField(unique=True, null=True)
    employees = models.ManyToManyField(Result, blank=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'training_result'


