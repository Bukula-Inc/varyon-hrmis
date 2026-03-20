from datetime import date
from django.db import models
from client_app.hr.employee.models import Employee

class Form_Of_Agreement_For_A_Personal_Loan_Witness(models.Model):
    witness = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    witness_name = models.CharField(max_length=255, null=True, default="")
    department  = models.CharField(max_length=255, null=True, default="")
    email = models.CharField(max_length=255, default="", null=True)

    class Meta:
         db_table = 'form_of_agreement_for_personal_loan_witness'

class Form_Of_Agreement_For_A_Personal_Loan(models.Model):
    name = models.CharField(max_length=255, unique=True, default="")
    date_of_agreement = models.DateField(null=True, default=date.today)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    employee_full_names = models.CharField(max_length=255, default="", null=True)
    email = models.CharField(max_length=255, null=True, default="")
    contact_no  = models.CharField(max_length=255, null=True, default="")
    maximum_loan_amount_loan_value  = models.FloatField(default=0.00, null=True)
    maximum_loan_amount_approved = models.FloatField(default=0.00, null=True)
    application = models.CharField (max_length=255, default="", null=True)
    ref_doc = models.CharField (max_length=255, default="", null=True)
    personal_loan_witnesses = models.ManyToManyField(Form_Of_Agreement_For_A_Personal_Loan_Witness, blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    class Meta:
        db_table = 'form_of_agreement_for_personal_loan'

    def __str__(self):
        return self.name