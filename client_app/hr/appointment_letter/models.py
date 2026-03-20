from django.db import models
from client_app.hr.interview.models import Interview
from client_app.models import BaseModel
from client_app.core.company.models import Company
from client_app.hr.job_offer.models import Job_Offer
from datetime import date
# from controllers.utils.dates import Dates

# dates =Dates()

class Appointment_Letter(BaseModel):
    name = models.CharField(null=True, unique=True, default="")
    job_offer = models.ForeignKey( Job_Offer, on_delete=models.DO_NOTHING, default=None, null=True)
    interview = models.ForeignKey(Interview, on_delete=models.DO_NOTHING, default=None, null=True)
    company = models.ForeignKey( Company, on_delete=models.DO_NOTHING, default=None, null=True)
    reporting_date =models.DateField(default=date.today, null=True)
    date = models.DateField(default=date.today, null=True)
    appointment_context = models.TextField(default="", null=True, max_length=255)
    designation = models.CharField (max_length=255, null=True, default="")
    applicant = models.CharField (max_length=255, null=True, default="")
    applicant_email = models.CharField (max_length=255, null=True, default="")

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'appointment_letter'



