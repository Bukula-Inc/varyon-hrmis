from django.db import models
from client_app.core.department.models import Department
from client_app.hr.employee.models import Employee
from client_app.hr.employment_type.models import Employment_Type
from client_app.payroll.house_loan_agreement.models import House_Loan_Agreement
from client_app.models import BaseModel
from datetime import date

class House_Loan_Application(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    full_name = models.CharField(max_length=255, null=True, default="")
    nrc = models.CharField(null=True, default="")
    date_of_birth = models.CharField(max_length=255,default="", null=True)
    employee_no = models.CharField(null=True, default="")
    substantive_appointment = models.CharField(null=True, default="")
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, default="")
    date_of_engagement = models.CharField(max_length=255,default="", null=True)
    requested_amount = models.FloatField (default=0.00, null=True)
    requested_amount_words = models.CharField(max_length=255, null=True, default="")
    on_permanent_and_pensionable = models.IntegerField(null=True, default=0)
    on_secondment = models.IntegerField(null=True, default=0)
    contract_expiration_date = models.CharField(max_length=255,default="", null=True)
    sketched_building_plan = models.TextField(null=True, default="")
    approved_house_plan = models.TextField(null=True, default="")
    proof_of_ownership = models.TextField(null=True, default="")
    letter_of_sale = models.TextField(null=True, default="")
    # wittiness_staff = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, related_name="wittiness_staff", null=True, default=None)
    applicant_witness = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, related_name="wittiness_staff", null=True, default=None)
    cleared = models.IntegerField (default=0, null=True)
    interest_amount = models.FloatField (default=0.00, null=True)
    has_witnesses = models.IntegerField (default=0, null=True)
    total_amount_repaid = models.FloatField (default=0.00, null=True)
    basic_pay = models.FloatField (default=0.00, null=True)
    years_in_service_remaining = models.CharField (max_length=255, null=True, default="")
    age_to_retirement = models.CharField (max_length=255, null=True, default="")
    repayment_period = models.IntegerField (default=0, null=True)
    requested_amount = models.FloatField (default=0.00, null=True)
    is_amount_within_entitlement = models.CharField (default="", null=True, max_length=255)
    submitted_date = models.CharField(max_length=255,default="", null=True)
    approved_amount = models.FloatField (null=True, default=0.00)
    retirement_date = models.CharField (max_length=255, null=True, default="")
    service_condition_type = models.ForeignKey (Employment_Type, on_delete=models.DO_NOTHING, null=True, default=None)
    house_agreement = models.ForeignKey (House_Loan_Agreement, on_delete=models.DO_NOTHING, null=True, default=None)
    agreement = models.CharField (max_length=255, default="", null=True)
    ref_doc = models.CharField (max_length=255, default="", null=True)
    is_approved = models.IntegerField (null=True, default=0)
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "house_loan_application"