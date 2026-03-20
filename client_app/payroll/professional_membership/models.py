from django.db import models
from client_app.models import BaseModel
from client_app.hr.employee.models import Employee
from datetime import date


class Professional_Membership_Subscription (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    fullname = models.CharField (max_length=255, null=True, default="")
    section = models.CharField (max_length=255, null=True, default="")
    nrc = models.CharField (max_length=255, null=True, default="")
    submittion_date = models.DateField (null=True, default=date.today)
    designation = models.CharField (max_length=255, null=True, default="")
    salary_grade = models.CharField (max_length=255, null=True, default="")
    department = models.CharField (max_length=255, null=True, default="")
    amount = models.CharField (max_length=255, null=True, default="")
    membership_type = models.CharField (max_length=255, null=True, default="")
    name_of_professional_body = models.CharField (max_length=255, null=True, default="")
    account_name = models.CharField (max_length=255, null=True, default="")
    account_number = models.CharField (max_length=255, null=True, default="")
    sort_core = models.CharField (max_length=255, null=True, default="")
    invoice_number = models.CharField (max_length=50, null=True, default="")
    original_attachment = models.TextField (null=True, blank=True, default="")
    subscrition_attachment = models.TextField (null=True, blank=True, default="")
    amount_in_words =models.CharField (max_length=255, null=True, default="")
    requested_amount =models.FloatField (null=True, default=0.00)
    instalments_period =models.CharField (max_length=255, null=True, default="")
    branch_code = models.CharField (max_length=255, null=True, default="")
    desclaimer =models.IntegerField(default=0, null=True)
    cleared = models.IntegerField (default=0, null=True)
    total_amount_repaid = models.FloatField (default=0.00, null=True)
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'professional_membership_subscription'
