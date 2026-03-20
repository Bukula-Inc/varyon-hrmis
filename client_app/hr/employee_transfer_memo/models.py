from django.db import models
from datetime import date
from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel
from client_app.core.branch.models import Branch

class Employee_Transfer_Memo (BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True)
    employee_name = models.CharField(max_length=255, default="",null=True)
    transfer_employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True,related_name="employee_transferred")
    transfer_employee_name = models.CharField(max_length=255, default="",null=True)
    transfer_date = models.DateField (default=date.today, null=True)
    new_off_report_date = models.DateField (default=date.today, null=True)
    new_location = models.ForeignKey (Branch, on_delete=models.DO_NOTHING, null=True, default=None)
    from_location = models.ForeignKey (Branch, on_delete=models.DO_NOTHING, null=True, default=None, related_name="from_location")
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None,null=True)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None,null=True)
    transfer_employee_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None,null=True, related_name="reans_dept")
    transfer_employee_designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None,null=True, related_name="reans_desig")
    staff_id = models.CharField(max_length=255, default="", null=True)
    pay_settling_in_allowance = models.IntegerField (default=0, null=True)
    transfer_purpose = models.TextField (blank=True, null=True, default="")

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee_transfer_memo'



