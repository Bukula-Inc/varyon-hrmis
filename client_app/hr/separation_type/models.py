from django.db import models

# Create your models here.
from client_app.payroll.allowance_and_benefit.models import Allowance_and_Benefit
from client_app.hr.exit_interview_question.models import Exit_Interview_Question
from client_app.models import BaseModel, TableModel

class Separation_Severance_Package(TableModel):
    package_item =models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table ="separation_severance_package"


class Separation_Package(TableModel):
    package_item =models.ForeignKey(Allowance_and_Benefit, on_delete=models.DO_NOTHING, default=None, null=True, related_name="allowance_and_benefit")
    class Meta:
        db_table ="separation_package"

class Separation_Type(BaseModel):
    name =models.CharField(max_length=255, default="", null=True)
    includes_severance_package =models.IntegerField(default=0.00, null=True)
    severance_package =models.ManyToManyField(Separation_Severance_Package, blank=True)

    # NEW FIELDS TO KEEP
    interview_question =models.ForeignKey(Exit_Interview_Question, on_delete=models.DO_NOTHING, default=None, null=True)
    description =models.TextField(default="", null=True)
    separation_package =models.ManyToManyField(Separation_Package, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table ="separation_type"