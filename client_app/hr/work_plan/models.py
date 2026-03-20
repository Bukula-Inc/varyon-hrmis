from django.db import models
from client_app.core.company.models import Company
from client_app.hr.employee.models import Employee
from datetime import date
from client_app.models import BaseModel, TableModel

class Work_Plan_Task(TableModel):
    title = models.CharField(max_length=255, null=True, default="")
    planer_of_work_plan = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    description = models.TextField(null=True, default="")
    out_come = models.TextField(null=True, default="")
    expected_start_date = models.DateField(null=True, default=date.today)
    expected_end_date = models.DateField(null=True, default=date.today)
    started_on = models.DateField(null=True, default=date.today)
    completed_on = models.DateField(null=True, default=date.today)
    task_status = models.CharField(max_length=255, null=True, default="")
    progress_tracker = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'work_plan_tasks'

class Work_Plan(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None,null=True)
    employee_name = models.CharField(max_length=255,null=True,default="")
    period = models.CharField(max_length=255,null=True,default="")
    sales_plan_for = models.CharField(max_length=255,null=True,default="")
    goal_and_objectives = models.TextField (default='', null=True, blank=True)
    is_current = models.IntegerField(null=True,default=0)
    quarter = models.CharField(max_length=255,null=True,default="")
    month = models.CharField(max_length=255,null=True,default="")
    work_plan_task = models.ManyToManyField(Work_Plan_Task, blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'work_plan'

class Performance_Agreement (BaseModel):
    name = models.CharField(max_length=255, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    full_name = models.CharField(max_length=255,null=True,default="")
    first_name = models.CharField(max_length=255,null=True,default="")
    middle_name = models.CharField(max_length=255,null=True,default="")
    last_name = models.CharField(max_length=255,null=True,default="")
    report_to = models.CharField(max_length=255,null=True,default="")
    is_active = models.CharField (max_length=255, default="", null=True)
    performance_kpi = models.JSONField (default=list, null=True, blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'performance_agreement'

class Request_Task_Adjustment (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    work_plan = models.ForeignKey (Performance_Agreement, on_delete=models.DO_NOTHING, null=True, default=None)
    title = models.CharField(max_length=255, null=True, default="")
    expected_start_date = models.DateField(null=True, default=date.today)
    expected_end_date = models.DateField(null=True, default=date.today)
    description = models.TextField(null=True, default="")
    reason = models.TextField(null=True, default="")
    used =models.IntegerField (default=0, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'request_task_adjustment'
