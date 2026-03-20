from django.db import models
from client_app.models import BaseModel
from client_app.core.company.models import Company
from client_app.models import BaseModel, TableModel
from client_app.core.company.models import Company
from client_app.hr.employee.models import Employee
from client_app.hr.training_program.models import Training_Program
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from datetime import date

class Resource_Files(TableModel):
    attachment = models.TextField (default='', blank=True)
    media_type =models.CharField (max_length=255, default="", null=True)

    class Meta:
        db_table = 'resource_files'

class Training_Resources(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    training_program = models.ForeignKey(Training_Program, on_delete=models.DO_NOTHING, default=None,null=True)
    # file_group = models.ForeignKey(File_Group, on_delete=models.DO_NOTHING, default=None,null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None,null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None,null=True)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None,null=True)
    files = models.ManyToManyField(Resource_Files, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'training_resources'
