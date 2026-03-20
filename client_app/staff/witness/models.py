# from django.db import models
# from client_app.models import BaseModel, TableModel
# from client_app.hr.employee.models import Employee
# from client_app.authentication.models import Lite_User
# from client_app.hr.skills.models import Skills
# from client_app.hr.training_program.models import Training_Program 

# # Create your models here.

# class Employees_Lacking_Skill(TableModel):
#     employee =models.ForeignKey(Employee, on_delete=models.DO_NOTHING,default=None, null=True)
#     employee_full_name =models.CharField(max_length=255, default="", null=True)

#     class Meta:
#         db_table ="employees_lacking_skill"


# class Skill_Gap(BaseModel):
#     name =models.CharField(max_length=255, default="", unique=True, null=True)
#     Initiator =models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING,default=None, null=True)
#     skill =models.ForeignKey(Skills, on_delete=models.DO_NOTHING,default=None, null=True)
#     training_program =models.ForeignKey(Training_Program, on_delete=models.DO_NOTHING,default=None, null=True)
#     employees_lacking_the_skill =models.ManyToManyField(Employees_Lacking_Skill, blank=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table ="skill_gap"
