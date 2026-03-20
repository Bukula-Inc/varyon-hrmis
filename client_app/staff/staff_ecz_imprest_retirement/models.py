from django.db import models
from client_app.core.company.models import Company
from client_app.core.country.models import Country
from client_app.core.currency.models import Currency
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel, TableModel
from datetime import date
from client_app.hr.employee.models import Employee
# from client_app.staff.
# Create your models here.



class Imprest_Visited_Province(TableModel):
    province =models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table ="imprest_visited_province"

class Imprest_Visited_District(TableModel):
    district =models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table ="imprest_visited_district"


class ECZ_Retirement_Item(TableModel):
    description =models.TextField(default="", null=True)
    amounts =models.FloatField(default=0.00, null=True)

    class Meta:
        db_table ="ecz_retirement_item"


class ECZ_Imprest(BaseModel):

    name =models.CharField(max_length=255, default="", null=True)
    request_date =models.DateField(default=date.today, null=True)
    initiator =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ecz_imprest")
    initiator_first_name =models.CharField(max_length=255, default="", null=True)
    initiator_last_name =models.CharField(max_length=255, default="", null=True)
    job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ecz_imprest_designation")
    annual_salary =models.FloatField(default=0.00, null=True)
    country =models.ForeignKey(Country, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ecz_imprest_country")
    duration_from_date =models.DateField(default=date.today, null=True)
    duration_to_date =models.DateField(default=date.today, null=True)

    province_visited =models.ManyToManyField(Imprest_Visited_Province, blank=True)
    district_visited =models.ManyToManyField(Imprest_Visited_District, blank=True)
           
    nature_of_offical_duty =models.TextField(default="", null=True)
    mode_of_travel =models.CharField(max_length=255, default="", null=True)
    registration_number_of_vechile =models.CharField(max_length=255, default="", null=True)
    vechile_make =models.CharField(max_length=255, default="", null=True)
    estimated_cost_of_travel =models.FloatField(default=0.00, null=True)

    retirement_item =models.ManyToManyField(ECZ_Retirement_Item, blank=True)

    request_currency =models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=None, null=True,related_name="request_currency")
    requested_amount =models.FloatField(default=0.00, null=True)
    # requested_to_reporting_currency_convertion_rate =models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=None, null=True, related_name="requested_to_reporting_currency_convertion_rate")
    approved_amount =models.FloatField(default=0.00, null=True)
    requested_amount_in_reporting_currency =models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=None, null=True, related_name="requested_amount_in_reporting_currency")
            # approved_to_reporting_currency_convertion_rate =models.CharField(max_length=255, default="", null=True)
    company =models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True,)
    is_added_to_payment_requisition =models.CharField(max_length=255, default="", null=True)
    retired_amount =models.CharField(max_length=255, default="", null=True)
    # retired_amount_in_reporting_currency =models.CharField(max_length=255, default="", null=True)
    balance =models.CharField(max_length=255, default="", null=True)
    # balance_in_reporting_currency =models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="ecz_imprest"

# RETIREMENT


class Imprest_Areas_of_Expense(TableModel):
    subsistance_allowance =models.CharField(max_length=255, default="", null=True)
    usage_length =models.FloatField(default=0, null=True)
    unit_price_of_usage =models.FloatField(default=0, null=True)
    total_spent =models.FloatField(default=0, null=True)
    expense_attachment =models.TextField(default="", null=True)

    class Meta:
        db_table ="imprest_areas_of_expense"

class Imprests_Places_Visited(TableModel):
    place =models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table ="imprests_places_visited"


class ECZ_Imprest_Retirement(BaseModel):

    name =models.CharField(max_length=255, default="", null=True)
    employee_no =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ecz_imprest_retirement")
    surname =models.CharField(max_length=255, default="", null=True)
    other_name =models.CharField(max_length=255, default="", null=True)
    position =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ecz_imprest_retirement_position" )
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ecz_imprest_retirement_dep" )
    section =models.CharField(max_length=255, default="", null=True)
    imprest =models.ForeignKey(ECZ_Imprest, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ecz_imprest_retirement_imprest" )
    duration_of_tour_from =models.DateField(default=date.today, null=True)
    duration_of_tour_to =models.DateField(default=date.today, null=True)
    registration_vehicle =models.CharField(max_length=255, default="", null=True)
    vehicle_model =models.CharField(max_length=255, default="", null=True)


    places_visited =models.ManyToManyField(Imprests_Places_Visited, blank=True)
    areas_of_expense =models.ManyToManyField(Imprest_Areas_of_Expense, blank=True)


    retired_amount =models.FloatField(default=0.00, null=True)
    balance_left =models.FloatField(default=0.00, null=True)
    imprest_obtained =models.FloatField(default=0.00, null=True)
    pending =models.FloatField(default=0.00, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="ecz_imprest_retirement"