import datetime
from datetime import datetime, timezone
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from datetime import datetime
import pandas as pd

utils = Utils ()
pp = utils.pretty_print
class Employee_seperation_dashboard:
    def __init__(self, dbms, object) -> None:
        self.dbms = dbms
        self.object = object
        self.core_hr = Core_Hr (dbms=self.dbms)

    @classmethod
    def employee_separation(cls, dbms, object):
        cls.__init__ (cls, dbms=dbms, object=object)
        return utils.respond (utils.ok, {"employee_separation": cls.employees(cls),"init_emp_seperation": cls.init_seperation(cls),
            "employee_separation_by_designation": cls.calculate_separation_percentage(cls),"pending_exit_interview": cls.pending_exit_interview(cls), "final_statement_stats": cls.get_employees_with_unsettled_assets(cls),})
    def employees(self):
        get_employee_separations = self.core_hr.get_employee_list()
        if get_employee_separations:
            total_seperation = 0
            terminated_count = 0
            total_resigned_emp = 0
            total_employees = len(get_employee_separations)

            for employee in get_employee_separations:
                if employee.get("is_separated", 0) == 1:
                    status = employee.get("status", "").lower()
                    if "terminated" in status or "resigned" in status or "left" in status:
                        total_seperation += 1                    
                    if "terminated" in status:
                        terminated_count += 1
                    if "resigned" in status:
                        total_resigned_emp += 1
            resigned_percentage = (total_resigned_emp / total_employees) * 100 if total_employees else 0

            return {
                "total_seperation": total_seperation,
                "total_terminated": terminated_count,
                "total_resigned_emp": total_resigned_emp,
                "total_resignation_percentage": round(resigned_percentage, 2),  
            }

            
    def init_seperation(self):
        init_separation = self.dbms.get_list("employee_separation", fetch_linked_tables=True)
        if init_separation.status == utils.ok:
            emp_data = init_separation.data.rows
            designation_counts = {}
            for emp in emp_data:
                designation = emp.get('designation', 'Unknown')  
                designation_counts[designation] = designation_counts.get(designation, 0) + 1
            response = {
                "designations": list(designation_counts.keys()),  
                "employee_counts": list(designation_counts.values()) 
            }
            
            return response

        return {"designations": [], "employee_counts": []} 

    def calculate_separation_percentage(self):
        get_employee_seperations = self.core_hr.get_employee_list()
        if get_employee_seperations:
            designation_data = {}
            for employee in get_employee_seperations:
                designation = employee["designation"] or "Unknown"
                is_separated = employee["is_separated"]
                if designation not in designation_data:
                    designation_data[designation] = {"total": 0, "separations": 0}
                designation_data[designation]["total"] += 1
                if is_separated:
                    designation_data[designation]["separations"] += 1
            separation_percentages = {
                designation: (data["separations"] / data["total"]) * 100
                for designation, data in designation_data.items()
            }
            return separation_percentages
    def pending_exit_interview(self):
        get_final_stats = self.core_hr.employee_separation()
        exit_interview = self.core_hr.get_exit_interview()        
        interviewed_names = [interview['employee_name'] for interview in exit_interview]        
        pending_interviews = []
        if get_final_stats:
            for emp in get_final_stats:
                if emp['skip_exit_interview'] == 0: 
                    name = emp['employee_name']
                    if name not in interviewed_names:  
                        pending_interviews.append({"employee_name": name})         
        return pending_interviews
    def get_employees_with_unsettled_assets(self):
        get_final_stats = self.core_hr.final_statement(fetch_linked_tables=True)
        unsettled_employees = []
        if get_final_stats:
            for statement in get_final_stats:
                if statement['asset']:
                    has_unsettled_assets = any(
                        asset['assets_status'] is None or 
                        asset['assets_status'] != 'Settled'
                        for asset in statement['asset']
                    )
                    
                    if has_unsettled_assets:
                        unsettled_employees.append({
                            'employee_name': statement['employee_name'],
                            'unsettled_assets': [
                                {
                                    'component': asset['assets_component'],
                                    'status': asset['assets_status'],
                                    'amount': asset['assets_amount']
                                }
                                for asset in statement['asset']
                                if asset['assets_status'] is None or asset['assets_status'] != 'Settled'
                            ]
                        })
            
        return unsettled_employees


         

                            

            
