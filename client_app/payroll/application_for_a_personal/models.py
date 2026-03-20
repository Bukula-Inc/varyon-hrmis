from django.db import models
from client_app.core.currency.models import Currency
from client_app.core.department.models import Department
from client_app.models import BaseModel, TableModel
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Employee
from datetime import date

# Create your models here.
def default_list():
    return list


# class Personal_Loan_Witness(TableModel):
#     council_witness =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_witness_council")
#     applicant_witness =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_witness_applicatant")

#     class Meta:
#         db_table ="personal_loan_witness"


class Personal_Loan_Agreement(BaseModel):
    name =models.CharField(max_length=255, unique=True, null=True, default="")
    employee_full_name =models.CharField(max_length=255, default="", null=True)
    # requested_loan_amount_in_words =models.CharField(max_length=255, default="", null=True)

    # current_basic =models.FloatField(default=0.00, null=True)
    approved_loan =models.FloatField(default=0.00, null=True)

    date_of_agreement =models.DateField(default=date.today, null=True)

    employee_no =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_agreement_employee")
    job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_agreement_job_title")
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_agreement_department")
    council_witness =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_agreement_witness_council")
    applicant_witness =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_agreement_witness_applicatant")
    staff_id = models.ForeignKey (Employee, default=None, null=True, on_delete=models.DO_NOTHING, related_name="personal_loan_agreement_staff_id")
    application = models.CharField (max_length=255, default="", null=True)
    # witness =models.JSONField(default=default_list(), null=True)
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="personal_loan_agreement"


class Personal_Loan_Application(BaseModel):
    name =models.CharField(max_length=255, unique=True, null=True, default="")
    employee_full_name =models.CharField(max_length=255, default="", null=True)
    requested_loan_amount_in_words =models.CharField(max_length=255, default="", null=True)
    service_condition =models.CharField(max_length=255, default="", null=True)
    requested_repayment_period =models.IntegerField(default=0, null=True)
    agreement = models.CharField (max_length=255, default="", null=True)
    ref_doc = models.CharField (max_length=255, default="", null=True)
    approved_amount =models.FloatField(default=0.00, null=True)
    current_basic =models.FloatField(default=0.00, null=True)
    requested_loan_amount =models.FloatField(default=0.00, null=True)

    cleared =models.IntegerField(default=0, null=True)
    has_witnesses =models.IntegerField(default=0, null=True)

    date_of_application =models.DateField(default=date.today, null=True)
    date_of_end_of_contract =models.DateField(default=date.today, null=True)
    date_of_retirement =models.DateField(default=date.today, null=True)
    date_of_expiry_of_secondment =models.DateField(default=date.today, null=True)
    interest_amount = models.FloatField (default=0.00, null=True)
    employee_no =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_application_employee")
    job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_application_job_title")
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_application_department")
    # agreement =models.ForeignKey(Personal_Loan_Agreement, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_application_agreement") 
    council_witness =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_application_witness_council")
    applicant_witness =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="personal_loan_application_witness_applicatant")
    total_amount_repaid = models.FloatField (default=0.00, null=True)
    # witness =models.JSONField(default=default_list(), null=True)
    personal_agreement = models.ForeignKey (Personal_Loan_Agreement, on_delete=models.DO_NOTHING, null=True, default=None)
    is_approved = models.IntegerField (null=True, default=0)
    staff_id = models.CharField (max_length=255, default="", null=True)
    recovery_period = models.IntegerField (default=0.00, null=True)

    def __str__(self):
        return self.name
    
    class Meta:

        db_table ="personal_loan_application"