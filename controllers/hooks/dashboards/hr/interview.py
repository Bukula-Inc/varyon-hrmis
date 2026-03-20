from datetime import date
from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates
from datetime import datetime, timedelta

utils = Utils()
dates = Dates()
pp =utils.pretty_print

class Interview:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
    
    @classmethod
    def interview_side_view(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        return utils.respond(utils.ok,{
            "interview_info": cls.get_interview_info(cls),
            "interview_stats": cls.get_interview_stats(cls),
           
        })
    
    def get_interview_info(self):
        today = date.today()
        one_week_from_today = today + timedelta(days=7)
        interviews = self.dbms.get_list("Interview", fetch_linked_fields=True, user=self.user)
        if interviews:
            interview_data = interviews.data.rows
            result = []  
            for applicant in interview_data:
                schedule_date = applicant.schedule or None    
                if schedule_date !=None:     
                    if today <= schedule_date <= one_week_from_today:
                        applicant_name = applicant.linked_fields.application.applicant_name
                        result.append({
                            "applicant_name": applicant_name,
                            "schedule_date": schedule_date
                        })                    

            return result

        return []

    
    def get_interview_stats(self):
        
        interview_stats = []
        pending = 0
        accepted = 0
        rejected = 0

        staffing_plan = self.dbms.get_list("Staffing_Plan", filters={"status__in":["Submitted"]}, user=self.user)
        if staffing_plan.get("status") == utils.ok and staffing_plan.get("data").get("rows") and len(staffing_plan.get("data").get("rows")) > 0:
            for plan in staffing_plan.get("data").get("rows"):
                from_date = plan['from_date']
                to_date = plan['to_date']
                interviews = self.dbms.get_list("Interview", filters={"created_on__range": [from_date, to_date]}, user=self.user)
                if interviews.get("status") == utils.ok:
                    if len(interviews.get("data").get("rows")) > 0:
                        for interview in interviews.get("data").get("rows"):
                            if interview['status'] == 'Pending':
                                pending += 1
                            elif interview['status'] == 'Submitted':
                                accepted += 1
                            elif interview['status'] == 'Rejected':
                                rejected += 1

            interview_stats.append({
                "pending": pending,
                "accepted": accepted,
                "rejected": rejected,
            })

        return interview_stats
     



       
