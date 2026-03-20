from django.db import models
from client_app.models import BaseModel, TableModel
from client_app.hr.employee.models import Employee
from datetime import date

class Sitting_Members_Claim (TableModel):
    member = models.CharField (max_length=255, null=True, default="")
    amount = models.FloatField (default=0.00, null=True)
    unit = models.IntegerField (default=1, null=True)
    nrc = models.CharField (max_length=20, default="", null=True)
    class Meta:
        db_table = 'sitting_members_claim'
    def __str__(self):
        return self.name

class Sitting_Allowance (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    claim_by = models.CharField (max_length=255, default="", null=True)
    claim_by_designation = models.CharField (max_length=255, default="", null=True)
    claim_date = models.DateField (default=date.today, null=True)
    meeting_date = models.DateField (default=date.today, null=True)
    meeting_name = models.CharField (max_length=255, default="", null=True)
    total_amount =models.FloatField(default=0.00, null=True)

    members = models.JSONField (default=list, null=True)
    staff_id = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="sitting_allowance_claim_staff_id")


    class Meta:
        db_table = 'sitting_allowance_claim'
    def __str__(self):
        return self.name