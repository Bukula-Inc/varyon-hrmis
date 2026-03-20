from django.db import models
from datetime import date
from client_app.models import BaseModel, TableModel
from client_app.hr.employee.models import Employee
from client_app.hr.leave_type.models import Leave_Type

class Leave_Schedule (BaseModel):
    name = models.CharField (unique=True, max_length=255, default='', null=True)
    department = models.CharField (max_length=255, default='', null=True)
    department_days = models.FloatField (default=0.00, null=True)
    days = models.FloatField (default=0.00, null=True)
    planner = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    planner_full_names = models.CharField (max_length=255, default='', null=True)
    leave_type = models.ForeignKey (Leave_Type, on_delete=models.DO_NOTHING, null=True, default=None)
    start_date = models.DateField (default=date.today, null=True)
    end_date = models.DateField (default=date.today, null=True)
    leave_information = models.JSONField (default=list, null=True, blank=True)
    is_active = models.IntegerField (default=0, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    class Meta:
        db_table = "leave_schedule"
    def __str__(self) -> str:
        return self.name