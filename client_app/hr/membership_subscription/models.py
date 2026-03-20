# from django.db import models

# from client_app.hr.employee.models import Employee
# from client_app.core.department.models import Department
# from client_app.hr.designation.models import Designation
# from client_app.core.company.models import Company
# from client_app.models import BaseModel , TableModel
# from client_app.payroll.employee_grade.models import Employee_Grade
# from datetime import date

# class Membership_Subscription(BaseModel):
#     name = models.CharField(unique=True, max_length=255, null=True)
#     employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True)
#     employee_name = models.CharField(max_length=255, default="",null=True)
#     salary_scale = models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
#     section = models.CharField(max_length=255, null=True, default="")
#     amount_in_words = models.CharField(max_length=255, null=True, default="")
#     department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None,null=True)
#     job_title = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None,null=True)
#     requested_amount = models.FloatField(default=0.00, null=True)
#     membership_type =models.CharField(max_length=255, default="",null=True)
#     professional_body =models.CharField(max_length=255, default="",null=True)
#     account_name =models.CharField(max_length=255, default="",null=True)
#     account_number =models.CharField(max_length=255, default="",null=True)
#     branch_code =models.CharField(max_length=255, default="",null=True)
#     sort_code =models.CharField(max_length=255, default="",null=True)
#     invoice_number =models.CharField(max_length=255, default="",null=True)
#     instalments_period =models.CharField(max_length=255, default="",null=True)
#     submittion_date =models.DateField(default=date.today, null=True)
#     subscrition_attachment =models.TextField(default="", null=True)

#     def __str__(self):
#         return self.name
#     class Meta:
#         db_table = 'professional_membership_subscription'