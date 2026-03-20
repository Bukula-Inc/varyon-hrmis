from django.db import models
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel
from datetime import date

class Long_Term_Sponsorship_Bonding_Period (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    agreement_date = models.DateField (default=date.today, null=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    program = models.CharField (max_length=255, default="", null=True)
    nrc = models.CharField (max_length=255, default="", null=True)
    applicant_names = models.CharField (max_length=255, default="", null=True)
    qualification = models.CharField (max_length=255, default="", null=True)
    application = models.CharField (max_length=255, default="", null=True)
    ref_doc = models.CharField (max_length=255, default="", null=True)
    start_date = models.DateField (default=date.today, null=True)
    end_date = models.DateField (default=date.today, null=True)
    wittiness_staff = models.CharField (max_length=255, default="", null=True,) 
    council_staff = models.CharField (max_length=255, default="", null=True,)    
    staff_id = models.CharField(max_length=255, default="", null=True)


    class Meta:
        db_table = 'long_term_sponsorship_bonding_period'


class Long_Term_Sponsorship (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    last_name = models.CharField (max_length=255, default="", null=True)
    first_name = models.CharField (max_length=255, default="", null=True)
    middle_name = models.CharField (max_length=255, default="", null=True)
    designation = models.CharField (max_length=255, null=True, default="")
    salary_grade = models.CharField (max_length=255, null=True, default="")
    department = models.CharField (max_length=255, null=True, default="")
    basic_pay = models.FloatField (default=0.00, null=True)
    age = models.CharField (max_length=4, default="", null=True)
    end_of_contract = models.DateField (default=date.today, null=True)
    course_of_study = models.CharField (max_length=255, null=True, default="")
    mode_of_study = models.CharField (max_length=255, null=True, default="")
    course_duration = models.CharField (max_length=255, null=True, default="")
    institution = models.CharField (max_length=255, null=True, default="")
    qualification_to_be_obtained = models.CharField (max_length=255, null=True, default="")
    reason = models.TextField (blank=True, null=True, default="")
    current_highest_qualification = models.TextField (blank=True, null=True, default="")
    current_job_responsibilities = models.TextField (blank=True, null=True, default="")
    boarding_and_lodging = models.FloatField (default=0.00, null=True)
    travel_costs = models.FloatField (default=0.00, null=True)
    lunch_allowance = models.FloatField (default=0.00, null=True)
    books_allowance = models.FloatField (default=0.00, null=True)
    tuition_fees = models.FloatField (default=0.00, null=True)
    others = models.FloatField (default=0.00, null=True)
    usage = models.JSONField (default=list, null=True)
    saved = models.IntegerField (default=0, null=True)
    bounding_period = models.ForeignKey (Long_Term_Sponsorship_Bonding_Period, on_delete=models.DO_NOTHING, related_name="lts_bpa", default=None, null=True)
    wittiness_staff = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, related_name="witness_staff", default=None, null=True)
    cleared = models.IntegerField (default=0, null=True)
    is_approved = models.IntegerField (default=0, null=True)
    has_witnesses = models.IntegerField (default=0, null=True)
    agreement = models.CharField (max_length=255, default="", null=True)
    ref_doc = models.CharField (max_length=255, default="", null=True)
    start_date = models.DateField (default=date.today, null=True)
    end_date = models.DateField (default=date.today, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'long_term_sponsorships'

class Long_Term_Sponsorship_Fund_Request (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    reference = models.ForeignKey (Long_Term_Sponsorship, on_delete=models.DO_NOTHING, default=None, null=True)
    boarding_and_lodging = models.FloatField (default=0.00, null=True)
    travel_costs = models.FloatField (default=0.00, null=True)
    lunch_allowance = models.FloatField (default=0.00, null=True)
    books_allowance = models.FloatField (default=0.00, null=True)
    tuition_fees = models.FloatField (default=0.00, null=True)
    others = models.FloatField (default=0.00, null=True)
    is_approved = models.IntegerField (default=0, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table = 'long_term_sponsorship_fund_request'