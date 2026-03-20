from django.db import models

# Create your models here.
from client_app.models import BaseModel, TableModel

class Open_Ended_Exit_Question(TableModel):
    question =models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table ="open_ended_exit_question"

class Closed_Ended_Exit_Question(TableModel):
    question =models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table ="closed_ended_exit_question"

class Exit_Interview_Question(BaseModel):
    name =models.CharField(max_length=255, default="", null=True)
    open_ended_questions =models.ManyToManyField(Open_Ended_Exit_Question, blank=True)
    closed_ended_questions =models.ManyToManyField(Closed_Ended_Exit_Question, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="exit_interview_question"