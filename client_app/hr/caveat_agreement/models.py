from django.db import models

from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel , TableModel
from datetime import date

class Caveat_Agreement_Witness(TableModel):
    witness_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True, related_name="witness_id")
    witness_name = models.CharField(max_length=255, default="",null=True)
    address = models.CharField(max_length=255, null=True, default="")
    occupation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None,null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'caveat_agreement_witness'

class Caveat_Agreement(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    council_representative = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True, related_name="council_representative")
    first_party = models.CharField(max_length=255, default="",null=True)
    Subdivision_2 = models.CharField(max_length=255, null=True, default="")
    Subdivision_a = models.CharField(max_length=255, null=True, default="")
    constraction_site_address = models.CharField(max_length=255, null=True, default="")
    authoriser = models.CharField(max_length=255, null=True, default="")
    paying_party = models.CharField(max_length=255, null=True, default="")
    council_representative_name = models.CharField(max_length=255, null=True, default="")    
    in_house_loan = models.FloatField(default=0, null=True)
    pay_sum = models.FloatField(default=0, null=True)
    reason_for_application =models.TextField(default="", null=True)
    agreement_date =models.DateField(default=date.today, null=True)
    council_enter_agreement_date =models.DateField(default=date.today, null=True)
    witness_list = models.ManyToManyField(Caveat_Agreement_Witness, blank=True,)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'caveat_agreement'

