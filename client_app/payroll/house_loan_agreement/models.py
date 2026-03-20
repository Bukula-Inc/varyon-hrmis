from django.db import models
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel
from datetime import date

class House_Loan_Agreement_Witness_List(TableModel):
    # name = models.CharField(max_length=255, unique=True, null=True)
    date_of_signing = models.CharField(max_length=255,default=date.today, null=True)
    witness = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="house_loan_agreementwitness")
    witness_name = models.CharField(max_length=255, null=True, default="")
    designation = models.CharField(null=True, default="")
    address = models.CharField(null=True, default="")
    on_behalf_of = models.CharField(null=True, default="")

    class Meta:
        db_table ="house_loan_agreement_witness_list"

class House_Loan_Agreement(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    date_of_agreement = models.CharField(max_length=255,default=date.today, null=True)
    borrower = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="borrower")
    borrowers_name = models.CharField(max_length=255, null=True, default="")
    advance_amount_in_words = models.CharField(null=True, default="")
    advance_amount = models.FloatField(null=True, default=0.00)
    location = models.CharField(null=True, default="")
    application = models.CharField (max_length=255, default="", null=True)
    ref_doc = models.CharField (max_length=255, default="", null=True)
    witnesses = models.ManyToManyField(House_Loan_Agreement_Witness_List, blank=True,)
    staff_id = models.CharField (max_length=255, default="", null=True)

    
    def __str__(self):
        return self.name
    class Meta:
        db_table = "house_loan_agreement"