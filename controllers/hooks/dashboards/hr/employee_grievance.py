from datetime import datetime
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class Employee_Grievance:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.core_hr = Core_Hr(dbms=dbms)

    @classmethod
    def grievance(cls, dbms, object):
        instance = cls(dbms, object)
        return utils.respond(utils.ok, {
            "grievance_list": instance.get_employee_grievance(),
            "get_grievances_generated_per_month": instance.get_grievances_generated_per_month(),
            "get_grievance_details": instance.get_grievance_details(),
            "get_most_common_grievance_details": instance.get_most_common_grievance_details(),
            "discipline_outcomes": instance.discipline_outcomes(),
            "most_recent_case_outcomes": instance.most_recent_case_outcomes(),
            "committee_performance": instance.committee_performance(),
        })  
    def get_employee_grievance(self): 
        grievance_list = self.core_hr.get_list("Employee_Grievance", privilege=True)
        if grievance_list:
            grievances_raised = len(grievance_list)
            resolved_grievances = sum(1 for grievance in grievance_list if grievance['status'] == 'Resolved')
            unresolved_grievances = grievances_raised - resolved_grievances
            
            return {
                "Grievances_Raised": grievances_raised,
                "Resolved_Grievances": resolved_grievances,
                "Unresolved_Grievances": unresolved_grievances
            }
    def get_grievances_generated_per_month(self):
        grievance = self.core_hr.get_list("Employee_Grievance", privilege=True)
        if grievance:
            monthly_grievances = {}
            for g in grievance:
                month = g['grievance_date'].strftime('%B')  
                if month in monthly_grievances:
                    monthly_grievances[month] += 1
                else:
                    monthly_grievances[month] = 1
            return [{"month": month, "number_of_g_raised": count} for month, count in monthly_grievances.items()]
    def get_grievance_details(self):
        grievance = self.core_hr.get_list("Employee_Grievance", privilege=True)
        if grievance:
            grievance_details = []
            for g in sorted(grievance, key=lambda x: x['grievance_date'], reverse=True)[:3]:
                grievance_id = g['subject'].split('-')[-1]
                raised_on = g['grievance_date'].strftime('%d %B %Y')
                status = g['status']

                details = {
                    "Grievance_ID": f"{grievance_id}",
                    "Raised_on": raised_on,
                    "Status": status
                }
                grievance_details.append(details)

            return grievance_details
    def get_committees(self):
        committees = self.core_hr.get_list("Disciplinary_Committee", privilege=True)
        if committees:
            for committee in committees:
                pass
    def get_most_common_grievance_details(self):
        get_common_grievance = self.core_hr.get_list("Employee_Grievance", privilege=True)
        if get_common_grievance:
            grievance_types = [g['grievance_type'] for g in get_common_grievance]
            grievance_counts = {}
            for g in grievance_types:
                if g in grievance_counts:
                    grievance_counts[g] += 1
                else:
                    grievance_counts[g] = 1
            most_common_grievance = max(grievance_counts, key=grievance_counts.get)
            return [
                {
                    "Most_Common_Grievance": most_common_grievance,
                    "Count": grievance_counts[most_common_grievance]
                }
            ]
    def discipline_outcomes(self):
        discipline_outcomes = self.core_hr.get_list("Case_Outcome", privilege=True)
        if discipline_outcomes:
            total_discipline_processed = len(discipline_outcomes)
            total_terminations_processed = sum(1 for outcome in discipline_outcomes if outcome['termination'] == '1')
            
            result = {
                "Total_number_of_Discipline_this_month": total_discipline_processed,
                "Total_number_of_terminations_this_month": total_terminations_processed
            }
            
            return result  
    def most_recent_case_outcomes(self):
        most_recent_cases = self.core_hr.get_list("Case_Outcome", privilege=True)
        if most_recent_cases:
            outcomes = {
                "termination": 0,
                "suspension": 0,
                "verbal_warning": 0,
                "written_warning": 0
            }
            
            for case in most_recent_cases:
                for outcome, value in case.items():
                    if value == "1" and outcome in outcomes:
                        outcomes[outcome] += 1
            
            return [
                {
                    "Outcome_Type": outcome_type.replace("_", " ").title(),
                    "Count": count
                } for outcome_type, count in outcomes.items()
            ]
    def committee_performance(self):
        committee_perf = self.core_hr.get_list("Employee_Grievance", privilege=True)
        total_grievances = len(committee_perf)
        resolved_grievances = len([grievance for grievance in committee_perf if grievance['status'] == 'Resolved'])
        performance_percentage = (resolved_grievances / total_grievances) * 100 if total_grievances > 0 else 0
        return performance_percentage


