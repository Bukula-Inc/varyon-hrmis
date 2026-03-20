from django.db import models


from client_app.hr.employee.models import Employee
from client_app.hr.interview_type.models import Interview_Type
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel , TableModel

class Round(TableModel):
    skill = models.CharField(unique=True, max_length=255, null=True)
    description = models.CharField(max_length=255, null=True, default="")

   
 
    def __str__(self):
        return f" {self.skill}"
    class Meta:
        db_table = 'round'





class Interview_Round(BaseModel):
    name = models.CharField(unique=True, null=True)
    interview_type = models.ForeignKey(Interview_Type, on_delete=models.DO_NOTHING, default=None, null=True, )
    interviewers= models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, )
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, )
    

    skillset= models.ManyToManyField(Round, blank=True)
   
    
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'interview_round' 



