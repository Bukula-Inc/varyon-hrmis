from django.db import models


from client_app.hr.appraisal_quarter.models import Appraisal_Quarter
from client_app.hr.appraisal_setup.models import Appraisal_Setup
from  client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.performance_agreement.models import Performance_Key_Area, Performance_Behavioral_Imperative
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel , TableModel
from client_app.core.company.models import Company
from datetime import date

def default_json_data():
    return {}

class Self_Appraisal_Behavioral_Imperatives_Performance (TableModel):
    desired_behavior = models.ForeignKey (Performance_Behavioral_Imperative, on_delete=models.DO_NOTHING, default=None)
    expected_behavior = models.TextField (default="", blank="", null=True)
    actual_behavior = models.TextField (default="", blank="", null=True)
    rating_b = models.IntegerField (default=0, null=True)
    comment = models.TextField (default="", blank="", null=True)
    def __str__(self):
        return f" {self.desired_behavior}"
    class Meta:
        db_table = 'self_appraisal_behavioral_imperatives_performance'



class Self_Appraisal_Performance_Agreement_KPIs (TableModel):
    strategic_goal = models.ForeignKey (Performance_Key_Area, on_delete=models.DO_NOTHING, default=None, null=True, related_name="self_appraisal_strategic_goal")
    thematic_area = models.ForeignKey (Performance_Key_Area, on_delete=models.DO_NOTHING, default=None, null=True, related_name="self_appraisal_thematic_area")
    key_result = models.CharField (max_length=255, default="", null=True)
    tasks_and_activities  = models.TextField (blank="", null=True)
    measure_and_indicator = models.TextField (blank="", null=True)
    from_date = models.DateField (default=date.today,null=True)
    to_date = models.DateField (default=date.today,null=True)
    rating_po = models.IntegerField (default=0, null=True)
    comment = models.TextField (blank=True, null=True)

    def __str__(self):
        return f" {self.strategic_goal}"
    class Meta:
        db_table = 'self_appraisal_performance_agreement_kpis'

class Self_Appraisal(BaseModel):
    name = models.CharField(unique=True,max_length=255,null=False, default="")
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
    appraisal_setup = models.ForeignKey(Appraisal_Setup, on_delete=models.DO_NOTHING, default=None, null=True)
    appraisee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    appraisee_name= models.CharField(max_length=255, default="", null=True)
    appraisal_closure_date = models.DateField(default=date.today)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, )
    appraisal_quarter = models.ForeignKey(Appraisal_Quarter, on_delete=models.DO_NOTHING, default=None, null=True)
    open_ended_questions = models.JSONField(default=default_json_data, null=True)
    closed_ended_questions = models.JSONField(default=default_json_data, null=True)
    overall_score = models.FloatField(default=0.00, null=True)
    total_questions = models.IntegerField(default=0, null=True)
    total_open_ended_questions = models.IntegerField(default=0, null=True)
    total_closed_ended_questions = models.IntegerField(default=0, null=True)
    total_closed_score = models.FloatField(default=0.00, null=True)
    total_open_score = models.FloatField(default=0.00, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'self_appraisal'

class Appraise_Your_Self (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee_id = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    full_name = models.CharField (max_length=255, default="", null=True)
    designation = models.ForeignKey (Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    salary_grade = models.CharField (max_length=144, default="", null=True)
    department = models.ForeignKey (Department, on_delete=models.DO_NOTHING, null=True, default="")
    date_of_previous_assessment = models.CharField (max_length=255, default="",null=True)
    score_earned_previously = models.CharField (max_length=10, default="", null=True)
    period_covered_for_the_assessment = models.CharField (max_length=255, null=True, default="")
    purpose_of_the_assessment = models.CharField (max_length=255, null=True, default="")
    behavioral_imperatives_score = models.FloatField (default=0.00, null=True)
    performance_objective_score = models.FloatField (default=0.00, null=True)
    behavioral_imperative = models.JSONField (default=list, null=True, blank=True)
    performance_kpi = models.JSONField (default=list, null=True,blank=True)
    bonus_amount = models.FloatField (default=0.00, null=True, blank=True)
    # behavioral_imperative = models.ManyToManyField (Self_Appraisal_Behavioral_Imperatives_Performance, blank=True)
    # performance_kpi = models.ManyToManyField (Self_Appraisal_Performance_Agreement_KPIs, blank=True)
    eligible_for_bonus = models.IntegerField (default=0, null=True)
    done = models.IntegerField (default=0, null=True)
    self_app_total_score = models.FloatField (default=0.00, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'appraise_your_self'