from django.db import models
from client_app.models import BaseModel, TableModel
from client_app.hr.leave_type.models import Leave_Type
from client_app.hr.employee.models import Employee

class Map_Leave_Settings (TableModel):
    leave_type = models.ForeignKey (Leave_Type, related_name="main_leave_leave_types", on_delete=models.DO_NOTHING, default=None, null=True)
    class Meta:
        db_table = 'leave_settings'

class Council_Witness (TableModel):
    witness = models.ForeignKey (Employee, related_name="employee_relation", on_delete=models.DO_NOTHING, default=None, null=True)
    witness_email = models.CharField (max_length=255, null=True, default="")
    
    class Meta:
        db_table = 'council_witness'

class Hr_Setting(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    retirement_age = models.IntegerField(null=True,default=0)
    working_days = models.IntegerField(null=True,default=0)
    working_hrs = models.IntegerField(null=True,default=0)
    is_leave_commutable = models.IntegerField (null=True, default=0)
    standard_working_hours = models.IntegerField(null=True,default=0)
    birthdays = models.IntegerField(null=True,default=0)
    anniversaries = models.IntegerField(null=True,default=0)
    holidays = models.IntegerField(null=True,default=0)
    medical_clearance = models.TextField(null=True, default="")
    police_clearance = models.TextField(null=True, default="")
    oath_of_secrecy = models.TextField(null=True, default="")
    holiday_frequency = models.CharField(max_length=255, null=True, default="")
    leave_notification = models.IntegerField(null=True,default=0)
    expense_approver_mandatory_claim = models.IntegerField(null=True,default=0)
    show_leave_departments = models.IntegerField(null=True,default=0)
    auto_encashment = models.IntegerField(null=True,default=0)
    restrict_backdated_leave_application = models.IntegerField(null=True,default=0)
    check_vacancies = models.IntegerField(null=True,default=0)
    send_interview_feedback = models.IntegerField(null=True,default=0)
    set_interview_reminder = models.IntegerField(null=True,default=0) 
    company_napsa_acc = models.CharField(max_length=255, null=True, default="") 
    company_nhima_acc = models.CharField(max_length=255, null=True, default="")   
    working_on_weekend = models.CharField (max_length=20, default='', null=True)
    saturday = models.IntegerField(null=True,default=0) 
    sunday = models.IntegerField(null=True,default=0) 

    main_leave = models.ForeignKey (Leave_Type, on_delete=models.DO_NOTHING, default=None, null=True)

    leave_settings = models.ManyToManyField (Map_Leave_Settings, blank=True)
    council_witnesses = models.ManyToManyField (Council_Witness, blank=True)

    
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'hr_setting'

class Witnesses_Doc (BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    doc =  models.CharField(max_length=255, null=True, default="")
    document_type = models.CharField (max_length=255, null=True)
    total_witnesses = models.IntegerField (default=0, null=True)
    total_witnessed = models.IntegerField (default=0, null=True)
    applicant = models.ForeignKey (Employee, related_name="employee_relation_to_witness", on_delete=models.DO_NOTHING, default=None, null=True)
    witnesses = models.JSONField (default=list, null=True)

    
    class Meta:
        db_table = 'witnesses_doc'

class Witnessing (BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    doc =  models.CharField(max_length=255, null=True, default="")
    document_type = models.CharField (max_length=255, null=True, default="")
    witnesses = models.ForeignKey (Employee, related_name="witnessed_by", on_delete=models.DO_NOTHING, default=None, null=True)
    employee = models.ForeignKey (Employee, related_name="applicant_of_doc", on_delete=models.DO_NOTHING, default=None, null=True)
    full_names = models.CharField (max_length=255, null=True, default="")
    w_full_names = models.CharField (max_length=255, null=True, default="")
    consent = models.CharField (max_length=255, null=True, default="")

    class Meta:
        db_table = 'witnessing'