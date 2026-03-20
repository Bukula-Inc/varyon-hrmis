from django.db import models
from client_app.hr.employee.models import Employee
from client_app.hr.leave_type.models import Leave_Type
from client_app.models import BaseModel
from datetime import date

class Leave_Commutation_Memo (BaseModel):
    name = models.CharField(max_length=255, default="", unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING,null=True, default=None)
    fullname = models.CharField(max_length=255,null=True, default="")
    leave_type = models.ForeignKey(Leave_Type, on_delete=models.DO_NOTHING,null=True, default=None)
    amount = models.FloatField(null=True, default=0.00)
    working_days = models.IntegerField(null=True, default=0)
    basic_pay = models.FloatField(null=True, default=0.00)
    commutated_days = models.FloatField(null=True, default=0.00)
    commutable_days =models.FloatField(null=True, default=0.00)
    reason = models.TextField (blank=True)
    commuted_on = models.DateField (default=date.today, null=True)
    balance = models.FloatField(null=True, default=0.00)
    approved = models.CharField (max_length=25, default="", blank=True, null=True)

    def __str__(self):
        return self.fullname
    class Meta:
        db_table = 'leave_commutation_memo'


# Create your models here.
class Leave_Commutation(BaseModel):
    name = models.CharField(max_length=255, default="", unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING,null=True, default=None)
    fullname = models.CharField(max_length=255,null=True, default="")
    leave_type = models.ForeignKey(Leave_Type, on_delete=models.DO_NOTHING,null=True, default=None)
    amount = models.FloatField(null=True, default=0.00)
    working_days = models.IntegerField(null=True, default=0)
    basic_pay = models.FloatField(null=True, default=0.00)
    commutated_days = models.FloatField(null=True, default=0.00)
    commutable_days =models.FloatField(null=True, default=0.00)
    reason = models.TextField (blank=True)
    memo = models.ForeignKey (Leave_Commutation_Memo, on_delete=models.DO_NOTHING, default=None, null=True)
    commuted_on = models.DateField (default=date.today, null=True)
    paid = models.CharField (max_length=255, default="Unsettled", null=True)
    balance = models.FloatField(null=True, default=0.00)
    approved = models.CharField (max_length=25, default="", blank=True, null=True)
    attachment = models.TextField (blank=True, null=True, default="")
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.fullname
    class Meta:
        db_table = 'leave_commutation'
