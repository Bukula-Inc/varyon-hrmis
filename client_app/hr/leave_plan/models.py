from django.db import models
from datetime import date
from client_app.models import BaseModel, TableModel
from client_app.hr.employee.models import Employee
from client_app.hr.leave_type.models import Leave_Type

class Leave_Plan_Handover (TableModel):
    task = models.CharField (max_length=255, default='', null=True)
    priority = models.CharField (max_length=50, default='', null=True)
    task_status = models.CharField (max_length=50, default='', null=True)
    given_to = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    description = models.TextField (null=True, default='', blank=True)

    class Meta:
        db_table = "leave_plan_handover"
    def __str__(self) -> str:
        return self.task

class Leave_Plan (BaseModel):
    name = models.CharField (unique=True, max_length=255, default='', null=True)
    planner = models.ForeignKey (Employee, related_name="leave_planner", on_delete=models.DO_NOTHING, null=True, default=None)
    handed_over_to = models.ForeignKey (Employee, related_name="task_handed_over_to", on_delete=models.DO_NOTHING, null=True, default=None)
    leave_type = models.ForeignKey (Leave_Type, on_delete=models.DO_NOTHING, null=True, default=None)
    communication = models.CharField (max_length=255, null=True, default='')
    email = models.CharField (max_length=255, null=True, default='')
    contact = models.CharField (max_length=255, null=True, default='')
    home_contact = models.CharField (max_length=255, null=True, default='')
    leave_plan_tasks = models.ManyToManyField (Leave_Plan_Handover, blank=True)
    from_date = models.DateField (default=date.today, null=True)
    to_date = models.DateField (default=date.today, null=True)
    days = models.IntegerField (default=0, null=True)
    tker = models.CharField (max_length=255, default='', null=True)
    auto_create_leave_application = models.IntegerField (default=0, null=True)
    days_before_from_date = models.CharField (default=0, null=True)
    leave_plan_file = models.TextField (default="", null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    class Meta:
        db_table = "leave_plan"
    def __str__(self) -> str:
        return self.name