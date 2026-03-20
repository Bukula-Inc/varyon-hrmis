from django.db import models
from client_app.models import BaseModel, TableModel
from client_app.hr.employee.models import Employee
from client_app.hr.training_program.models import Training_Program
from client_app.hr.training_event.models import Training_Event


class Training_Program_Attachment(TableModel):
    attachment_title= models.CharField(max_length=255, default="", null=True)
    attachment =models.TextField(default="", null=True)    
    class Meta:
        db_table ="training_program_attachment"

class Training_Feedback(BaseModel):
    name = models.CharField(unique=True, null=True, max_length=255, default="")
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    training_program = models.ForeignKey(Training_Program, on_delete=models.DO_NOTHING, null=True)

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////
    # LIST OF FIELDS TO DELETE
    training_event = models.ForeignKey(Training_Event, on_delete=models.DO_NOTHING, null=True)
    relevance = models.CharField(max_length=255, null=True, default="")
    content = models.CharField(max_length=255, null=True, default="")
    delivery = models.CharField(max_length=255, null=True, default="")
    organization = models.CharField(max_length=255, null=True, default="")
    overall = models.CharField(max_length=255, null=True, default="")
    suggestions = models.TextField(null=True, default="")
    impact_on_work = models.CharField(max_length=255, null=True, default="")
    file_url = models.TextField(null=True, default="")
    recommendation = models.CharField(max_length=255, null=True, default="")
    # END OF LIST
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////

    report_attachments =models.TextField(default="", null=True)
    other_attachments =models.ManyToManyField(Training_Program_Attachment, blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'training_feedback'
