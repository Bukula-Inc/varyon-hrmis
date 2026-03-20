from django.db import models
from client_app.hr.leave_type.models import Leave_Type
from client_app.models import BaseModel, TableModel

class Policy_Details(TableModel):
    policy_type = models.CharField(max_length=255, null=True)
    total_days_allocated_per_month = models.FloatField(null=True, default=0)
    annual_allocation = models.FloatField(null=True, default=0)

    def __str__(self):
        return f"{self.policy_type}"

    class Meta:
        db_table = 'policy_details'

class Leave_Policy(BaseModel):
    name = models.CharField(unique=True, null=True)
    leave_policy = models.CharField(max_length=255, default="", null=True)
    leave_policy_main_control = models.CharField(max_length=255, default="", null=True)
    enable_single_accrual = models.IntegerField(null=True, default=0)
    policy_for = models.CharField(max_length=255, null=True)  
    accruing_leave_type = models.ForeignKey(Leave_Type, related_name="accruing_leave_type_pcy", on_delete=models.DO_NOTHING, default=None, null=True)
    policy_details = models.ManyToManyField(Policy_Details, blank=True, related_name="leave_policy_config")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'leave_policy'