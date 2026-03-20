from datetime import datetime
import pandas as pd
from controllers.core_functions.hr import Core_Hr
from analytics.hr import HR_Analytics
from controllers.utils import Utils
from controllers.utils.dates import Dates
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class HR_Dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.core = Core_Hr(dbms,object.user, object)
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.analytics =  HR_Analytics(dbms, object)
        self.employees = []
        self.total_employees = 0

    @classmethod
    def dashboard(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        cls.get_employees(cls)
        return utils.respond(utils.ok,{
            "total_employees": cls.total_employees,
            "employees_by_designation": cls.get_employees_by_designation(cls),
            "employees_by_gender": cls.get_employees_by_gender(cls),
            "employees_by_department": cls.get_employees_by_department(cls),
            "employees_by_status": cls.get_employees_by_status(cls),
            "monthly_attendance": cls.get_monthly_attendance(cls),
            "leave_summary": cls.get_leave_summary(cls),
            "employees_disciplinary": cls.get_employees_disciplinary(cls),
            "employee_summary": cls.get_employee_summary(cls),
            
        })

    def get_employees(self):
        employees = self.core.get_employee_list()
        if not employees:
            self.employees = []
        else:
            self.employees = employees
            self.total_employees = len(self.employees)
        
    
    def get_employees_by_designation(self):
        results = {}
        mapped = {}
        designations = self.core.get_designation_list()
        if len(self.employees) > 0:
            grouped = self.analytics.group_employees_by_designation(self.employees, only_totals=True)
            if grouped and grouped.status == utils.ok:
                mapped = grouped.data
        
        if designations:
            for des in designations:
                results[des.name] = mapped.get(des.name, 0)
            return results
        results = mapped
        return results


    def get_employees_by_gender(self):
        results = {"Male": 0, "Female": 0}
        if len(self.employees) > 0:
            grouped = self.analytics.group_employees_by_gender(self.employees, only_totals=True)
            if grouped and grouped.status == utils.ok:
                return grouped.data
        return results
    

    def get_employees_by_department(self):
        results = {}
        mapped = {}
        departments = self.core.get_department_list()
        if len(self.employees) > 0:
            grouped = self.analytics.group_employees_by_department(self.employees, only_totals=True)
            if grouped and grouped.status == utils.ok:
                mapped =  grouped.data
        if len(departments):
            for dep in departments:
                results[dep.name] = mapped.get(dep.name, 0)
            return results
        results = mapped
        
        return results
    
    def get_employees_by_status(self):
        results = {}
        if len(self.employees) > 0:
            grouped = self.analytics.group_employees_by_status(self.employees, only_totals=True)
            if grouped and grouped.status == utils.ok:
                d = grouped.data
                results["active"] = d.get("Active")
                results["on_leave"] = d.get("On Leave")
                results["left"] = 0
                if d.get("Resigned"):
                    results["left"] += int(d.get("Resigned"))
                if d.get("Terminated"):
                    results["left"] += int(d.get("Terminated"))
        return results
    
    
    def get_leave_summary(self):
        leave_summary = self.core.get_leave_info()
        return leave_summary

    def get_employees_disciplinary(self):
        data = {
            "open_disciplinary_cases":0,
            "closed_disciplinary_cases":0,
            "open_grievance_cases":0,
            "closed_grievance_cases":0
        }
        grieve = self.core.get_list("Employee_Grievance", privilege=True)
        if grieve:
            for grieve_ in grieve:
                if grieve_.status == "Escalated To Disciplinary" or grieve_.status == "Submitted":
                    data["open_grievance_cases"] += 1
                elif grieve_.status == "Resolved":
                    data["closed_grievance_cases"] += 1

        discip = self.core.get_list("Employee_Disciplinary", privilege=True)
        if discip:
             for discip_ in discip:
                if discip_.status == "Draft" or discip_.status == "Pending Review":
                    data["open_disciplinary_cases"] += 1
                elif discip_.status == "Resolved":
                    data["closed_disciplinary_cases"] += 1
        return data
    


    def get_employee_summary(self):
        pass

    def get_monthly_attendance(self):
        pass
    
    