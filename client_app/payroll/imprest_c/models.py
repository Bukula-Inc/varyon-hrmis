from django.db import models
from client_app.core.company.models import Company
from client_app.core.country.models import Country
from client_app.core.currency.models import Currency
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel, TableModel
from datetime import date
from client_app.hr.employee.models import Employee

def default_json():
    return list
class Imprest_Form_20_C(BaseModel):

    name =models.CharField(max_length=255, default="", null=True)
    request_date =models.DateField(default=date.today, null=True)
    initiator =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="imprest_form_20_c")
    initiator_first_name =models.CharField(max_length=255, default="", null=True)
    initiator_last_name =models.CharField(max_length=255, default="", null=True)
    job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="imprest_form_20_c_designation")
    annual_salary =models.FloatField(default=0.00, null=True)
    country =models.ForeignKey(Country, on_delete=models.DO_NOTHING, default=None, null=True, related_name="imprest_form_20_c_country")
    duration_from_date =models.DateField(default=date.today, null=True)
    duration_to_date =models.DateField(default=date.today, null=True)

    visited_province_and_district =models.JSONField(default=default_json(), null=True)
    retirement_item =models.JSONField(default=default_json(), null=True)
           
    nature_of_offical_duty =models.TextField(default="", null=True)
    mode_of_travel =models.CharField(max_length=255, default="", null=True)
    registration_number_of_vechile =models.CharField(max_length=255, default="", null=True)
    vechile_make =models.CharField(max_length=255, default="", null=True)
    estimated_cost_of_travel =models.FloatField(default=0.00, null=True)

    request_currency =models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=None, null=True,related_name="imprest_form_20_c_request_currency")
    requested_amount =models.FloatField(default=0.00, null=True)
    approved_amount =models.FloatField(default=0.00, null=True)
    requested_amount_in_reporting_currency =models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=None, null=True, related_name="imprest_form_20_c_requested_amount_in_reporting_currency")
    company =models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True,)
    is_added_to_payment_requisition =models.CharField(max_length=255, default="", null=True)
    retired_amount =models.CharField(max_length=255, default="", null=True)
    balance =models.CharField(max_length=255, default="", null=True)
    not_retired= models.IntegerField (default=0, null=True)
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="imprest_form_20_c"