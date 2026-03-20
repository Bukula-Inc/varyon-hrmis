from django.db import models
from client_app.core.company.models import Company
from client_app.core.country.models import Country
from client_app.core.currency.models import Currency
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel, TableModel
from datetime import date
from client_app.hr.employee.models import Employee
from client_app.payroll.imprest_a.models import Imprest_Form_20_A
from client_app.payroll.imprest_b.models import Imprest_Form_20_B
from client_app.payroll.imprest_c.models import Imprest_Form_20_C
from client_app.payroll.petty_cash.models import Petty_Cash
# from client_app.staff.
# Create your models here.

def default_json():
    return list

class Expense_Retirement_Expense(TableModel):
    subsistance_allowance =models.CharField(max_length=255, default="", null=True)
    usage_length =models.FloatField(default="", null=True)
    unit_price_of_usage =models.FloatField(default="", null=True)
    total_spent =models.FloatField(default="", null=True)
    expense_attachment =models.TextField(default="", null=True)

    class Meta:
        db_table ="expense_retirement_expense"
class Expense_Retirement(BaseModel):

    name =models.CharField(max_length=255, default="", null=True)
    employee_no =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="retirement_employee")
    surname =models.CharField(max_length=255, default="", null=True)
    other_name =models.CharField(max_length=255, default="", null=True)
    position =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="retirement_position" )
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, related_name="retirement_department" )
    section =models.CharField(max_length=255, default="", null=True)
    retirement_type =models.CharField(max_length=255, default="", null=True)
    petty_cash =models.ForeignKey(Petty_Cash, on_delete=models.DO_NOTHING, default=None, null=True, related_name="retirement_petty_cash" )
    imprest_a =models.ForeignKey(Imprest_Form_20_A, on_delete=models.DO_NOTHING, default=None, null=True, related_name="retirement_imprest_a" )
    imprest_b =models.ForeignKey(Imprest_Form_20_B, on_delete=models.DO_NOTHING, default=None, null=True, related_name="retirement_imprest_b" )
    imprest_c =models.ForeignKey(Imprest_Form_20_C, on_delete=models.DO_NOTHING, default=None, null=True, related_name="retirement_imprest_c" )
    duration_of_tour_from =models.DateField(default=date.today, null=True)
    duration_of_tour_to =models.DateField(default=date.today, null=True)
    registration_vehicle =models.CharField(max_length=255, default="", null=True)
    vehicle_model =models.CharField(max_length=255, default="", null=True)
    pc_retirement_amount =models.FloatField(default=0.00, null=True)


    places_visited =models.JSONField(default=default_json(), null=True)
    areas_of_expense =models.JSONField(default=default_json(), null=True)
    # ManyToManyField(Expense_Retirement_Expense, blank=True)


    retired_amount =models.FloatField(default=0.00, null=True)
    balance_left =models.FloatField(default=0.00, null=True)
    imprest_obtained =models.FloatField(default=0.00, null=True)
    pending =models.FloatField(default=0.00, null=True)

    owed_to =models.CharField(max_length=255, default="", null=True)

    obtained_amount =models.FloatField(default=0.00, null=True)
    attachments =models.TextField(default="", null=True)
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="expense_retirement"