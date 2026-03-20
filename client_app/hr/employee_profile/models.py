# from django.db import models

# from client_app.hr.employee.models import Employee
# from client_app.core.department.models import Department
# from client_app.hr.designation.models import Designation
# from client_app.core.company.models import Company

# from client_app.models import BaseModel , TableModel
# from datetime import date

# # Create your models here.

# class Employee_Profle(BaseModel): 
#     name = models.CharField(max_length=255, default="",null=True, unique=True)
#     first_name = models.CharField(max_length=255, default="",null=True)
#     middle_name = models.CharField(max_length=255, default="",null=True)
#     last_name = models.CharField(max_length=255, default="",null=True)
#     full_name = models.CharField(max_length=255, default="",null=True)
#     gender = models.CharField(max_length=255, default="",null=True)
#     d_o_b = models.DateField(default=date.today, null=True)

#     id_no = models.CharField(max_length=255, default="",null=True)
#     nhima = models.CharField(max_length=255, default="",null=True)
#     napsa = models.CharField(max_length=255, default="",null=True)
#     tpin = models.CharField(max_length=255, default="",null=True)
#     # employment_type =models.ForeignKey(Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True)
#     company =models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
#     date_of_joining = models.DateField(default=date.today, null=True)
#     email = models.CharField(max_length=255, default="",null=True)
#     contact = models.CharField(default=0,null=True)
#     physical_address = models.CharField(default=0,null=True)
#     designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True)
#     # branch =  models.ForeignKey(Branch, on_delete=models.DO_NOTHING, default=None, null=True)
#     department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True)

#     report_to = models.CharField(max_length=255, default=None,null=True)
#     requisition = models.CharField(max_length=255, default=None,null=True)
#     basic_pay = models.CharField(max_length=255, null=True,default=None)
   
#     bank_name= models.CharField(max_length=255, null=True,default="")
#     account_no= models.CharField(max_length=255, null=True,default="")
#     sort_code= models.CharField(max_length=255, null=True,default="")
#     # employee_grade = models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
#     working_days = models.IntegerField(null=True,default=0)
    
#     def __str__(self):
#         return self.name
#     class Meta:
#         db_table = 'employee_profile'