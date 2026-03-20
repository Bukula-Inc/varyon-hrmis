from django.db import models
from client_app.models import BaseModel
from client_app.hr.employee.models import Employee
from datetime import date


class Cash_Repayment (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    repayment_type = models.CharField (max_length=255, null=True, default="")
    reference_model =models.CharField (max_length=255, null=True, default="")
    repayment_reference = models.CharField (max_length=255, null=True, default="")
    employee =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    loan_obtained =models.FloatField (null=True, default=0.00)
    due_amount =models.FloatField (null=True, default=0.00)
    repayment =models.FloatField (null=True, default=0.00)
    repaid_amount =models.FloatField (null=True, default=0.00)
    advance_application= models.CharField (max_length=255, default="", null=True)
    house_loan_application= models.CharField (max_length=255, default="", null=True)
    personal_loan_application= models.CharField (max_length=255, default="", null=True)
    professional_membership_subscription= models.CharField (max_length=255, default="", null=True)
    long_term_sponsorship= models.CharField (max_length=255, default="", null=True)
    medical_recovery= models.CharField (max_length=255, default="", null=True)
    tuition_advance= models.CharField (max_length=255, default="", null=True)
    attachment =models.TextField(default="", null=True)

    repayer = models.CharField (max_length=255, null=True, default="")
    
    staff_id = models.CharField (max_length=255, default="", null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'cash_repayment'
