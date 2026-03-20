from django.db import models

from client_app.models import BaseModel

class Leave_Type(BaseModel):
    name = models.CharField(unique=True, null=True, max_length=255, default='')
    maximum_leave_allocated = models.CharField(max_length=255,default=0)
    carry_forward = models.IntegerField(default=0,null=True)
    total_days_allocated_per_month = models.FloatField(default=0.00,null=True)
    is_compensatory = models.IntegerField(null=True, blank=True, default=0)
    is_commutable = models.IntegerField(null=True, blank=True, default=0)
    show_on_payslip = models.IntegerField(null=True, blank=True, default=0)
    leave_type_year = models.CharField (max_length=255, default='', null=True)
    leave_days_type = models.CharField (max_length=255, default='', null=True)
    is_on_probation = models.IntegerField (default=0, null=True)
    apply_on = models.CharField (max_length=255, default='', null=True)
    accrual_frequency = models.CharField (max_length=255, default='', null=True)
    allow_system_auto_accrual = models.IntegerField (default=0, null= True)
    maximum_carry_forward_days = models.FloatField(default=0.00, null= True)
    maximum_commutable_days = models.FloatField(default=0.00, null= True)
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'leave_type'