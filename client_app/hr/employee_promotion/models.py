from django.db import models


from client_app.models import BaseModel, TableModel
from client_app.core.company.models import Company
from client_app.hr.employee.models import Employee
from client_app.payroll.employee_grade.models import Employee_Grade
from client_app.payroll.salary_component.models import Salary_Component
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.core.role.models import Role
from datetime import date

class Promotion_Earning (TableModel):
    earning = models.ForeignKey (Salary_Component, on_delete=models.DO_NOTHING, null=True, default=None, related_name="promo_earning")
    # class Meta:
    #     db_table = 'promotion_earnings' 

class Promotion_Deduction (TableModel):
    deduction = models.ForeignKey (Salary_Component, on_delete=models.DO_NOTHING, null=True, default=None, related_name="promo_deduction")
    # class Meta:
        # db_table = 'promotion_deductions' 

class Employee_Promotion(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    promotion_date= models.DateField(default=date.today, null=True)
    employee =models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="promo_emp")
    employee_name = models.CharField(max_length=255,null=True, default="")
    designation = models.CharField (max_length=255, null=True, default="")
    department = models.CharField (max_length=255, null=True, default="")
    revised_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, related_name="promo_dept")
    current_basic = models.CharField(max_length=255,default=0, null=True)
    revised_basic = models.CharField(max_length=255,default=0, null=True)
    company = models.ForeignKey (Company, on_delete=models.DO_NOTHING, default=None, null=True, related_name="promo_company")
    promotion_options = models.CharField (max_length=255, null=True, default="")
    salary_promotion_options = models.CharField (max_length=255, null=True, default="")
    employee_grade = models.ForeignKey (Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True, related_name="promo_grade")
    terms_and_conditions = models.TextField (null=True, default="")
    role = models.ForeignKey (Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    earnings = models.ManyToManyField (Promotion_Earning, blank=True)
    deductions = models.ManyToManyField (Promotion_Deduction, blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'employee_promotion' 



