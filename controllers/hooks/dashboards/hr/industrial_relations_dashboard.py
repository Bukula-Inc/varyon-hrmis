import pandas as pd
from controllers.core_functions.hr import Core_Hr
from controllers.utils.dict_to_object import Dict_To_Object
from datetime import datetime, date, timedelta
from analytics.hr import HR_Analytics
from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Industrial_Relations_Dashboard:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.core = Core_Hr(dbms, object.user, object)
        self.analytics =  HR_Analytics(dbms, object)
    @classmethod
    def dashboard(cls, dbms, object):
        dashboard_instance = cls(dbms, object) 
        return utils.respond(utils.ok,{
            "employee_retentions": dashboard_instance.employee_turnover_and_retention(),
            "recent_grievances": dashboard_instance.recent_grievance_submission(),
            "grievance_types_per_month": dashboard_instance.grievance_by_type(),
            "descipline_by_department": dashboard_instance.discipline_by_department(),
            "get_grievance_stats": dashboard_instance.get_grievance_stats(),
            "recent_actions": dashboard_instance.recent_actions(),
            "grievances_by_status": dashboard_instance.grievances_by_status(),
            # "escalated_cases": dashboard_instance.escalated_cases(),
        })
    def escalated_cases(self):
        get_workplan = self.core.get_list("Employee_Grievance", fetch_linked_tables=True, privilege=True)
        if get_workplan:
            df = utils.to_data_frame(get_workplan)
            df['created_on'] = pd.to_datetime(df['created_on'])
            unresolved_issues = df[df['status'] != 'Resolved']            
            quarterly_escalation = {}            
            for quarter in range(1, 5):
                current_quarter_issues = unresolved_issues[unresolved_issues['created_on'].dt.quarter == quarter]
                grouped_by_escalation = current_quarter_issues.groupby('escalation')['id'].count().to_dict()
                quarterly_escalation[f"Q{quarter}"] = grouped_by_escalation
            return quarterly_escalation
                
    def employee_turnover_and_retention(self):
        total_terminated = 0
        total_suspended = 0
        total_resigned = 0
        total_retired = 0
        get_employee_infor = self.core.get_employee_list()
        if get_employee_infor is not None:
            for emp_retention in get_employee_infor: 
                if emp_retention['status'] == "Suspended":
                    total_suspended +=1
                elif emp_retention['status'] == "Terminated":
                    total_terminated+=1
                elif emp_retention['status'] == "Resigned":
                    total_resigned+=1
                elif emp_retention['status'] == "Retired":
                    total_retired+=1
            return {"Total Terminated": total_terminated,"Total Suspended": total_suspended,"Total Resigned": total_resigned,"Total Retired":  total_retired,}
    def recent_grievance_submission(self):
        get_recent_submitions = self.core.get_grievances()
        recent_grievance = []
        if get_recent_submitions is not None:
            for grieve in get_recent_submitions:
                if (date.today() - grieve['created_on']).days <= 30:recent_grievance.append({"employee_name": grieve['employee_name'],"department": grieve['department'],})
            return recent_grievance
    def grievance_by_type(self):
        grievance_type = self.core.get_grievances()
        grievance_in_month = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}
        if grievance_type is not None:
            for grievance in grievance_type:
                created_on = (grievance['created_on'])
                month = created_on.strftime("%b")
                grievance_in_month[month] += 1
        data = []
        for month, count in grievance_in_month.items():
            data.append({"month": month, "count": count})
        return data
    def discipline_by_department(self):
        grievance_type = self.core.get_grievances()
        discipline_by_department = {}
        if grievance_type is not None:
            for grievance in grievance_type:
                department = grievance['department']
                grievance_type_name = grievance['grievance_type']
                if department not in discipline_by_department:
                    discipline_by_department[department] = {}
                if grievance_type_name not in discipline_by_department[department]:
                    discipline_by_department[department][grievance_type_name] = 0
                discipline_by_department[department][grievance_type_name] += 1
        department_wise_data = {}
        for department, grievance_types in discipline_by_department.items():
            department_wise_data[department] = {}
            for grievance_type, count in grievance_types.items():
                department_wise_data[department][grievance_type] = count
        return department_wise_data
    def get_grievance_stats(self):
        grievance_ = self.core.get_grievances()
        grievance_stats = {}
        total_grievances = len(grievance_) if grievance_ else 0
        if grievance_ is not None:
            for grievance in grievance_:
                if grievance["status"] == "Resolved":
                    grievance_stats["total_resolved_grievances"] = grievance_stats.get("total_resolved_grievances", 0) + 1
                grievance_stats["total_grievances"] = grievance_stats.get("total_grievances", 0) + 1
            total_grievances_percentage = (grievance_stats.get("total_grievances", 0) / total_grievances) * 100 if total_grievances > 0 else 0
            total_resolved_grievances_percentage = (grievance_stats.get("total_resolved_grievances", 0) / total_grievances) * 100 if total_grievances > 0 else 0
            resolution_rate = (grievance_stats.get("total_resolved_grievances", 0) / grievance_stats.get("total_grievances", 0)) * 100 if grievance_stats.get("total_grievances", 0) > 0 else 0
            grievance_stats = {"total_grievances_percentage": round(total_grievances_percentage, 2), "total_resolved_grievances_percentage": round(total_resolved_grievances_percentage, 2),"resolution_rate": round(resolution_rate, 2)}
        return grievance_stats
    def recent_actions(self):
        get_recent_actions = self.core.get_case_outcome()
        recent_actions = []
        if get_recent_actions is not None:
            for action in get_recent_actions:
                action_type = ""
                if action["termination"] == "1":
                    action_type = "Termination"
                elif action["suspension"] == "1":
                    action_type = "Suspension"
                elif action["written_warning"] == "1":
                    action_type = "Written Warning"
                elif action["verbal_warning"] == "1":
                    action_type = "Verbal Warning"
                recent_actions.append({"name": action["name"], "action": action_type, "date": action["created_on"]})
        return recent_actions
    def grievances_by_status(self):
        get_grievance = self.core.get_list("Employee_Grievance", privilege=True)
        if get_grievance:
            df = utils.to_data_frame(get_grievance)
            grievances_by_status = df.groupby('status')['id'].count().to_dict()
            return grievances_by_status
        return []