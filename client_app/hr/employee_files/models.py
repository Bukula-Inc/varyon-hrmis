from django.db import models

from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.core.company.models import Company
from client_app.models import BaseModel , TableModel

class File_Group(BaseModel):
    name = models.CharField(unique=True, null=True)
    description = models.TextField( null=True, default="")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'file_group' 

class Employee_File_Content(TableModel):
    file_name = models.CharField (max_length=255, default="", null=True)
    attachment = models.TextField (default='', blank=True, null=True)
    class Meta:
        db_table = 'employee_file_content'

class Employee_File(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True)
    employee_name = models.CharField(max_length=255, default="",null=True)
    file_group = models.ForeignKey(File_Group, on_delete=models.DO_NOTHING, default=None,null=True)
    email = models.CharField(max_length=255, null=True, default="")
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None,null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None,null=True)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None,null=True)
    file_content = models.ManyToManyField(Employee_File_Content, blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee_file'



