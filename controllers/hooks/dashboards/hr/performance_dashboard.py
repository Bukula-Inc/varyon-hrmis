import pandas as pd
from datetime import datetime
from controllers.core_functions.hr import Core_Hr
from controllers.utils.dict_to_object import Dict_To_Object
from analytics.hr import HR_Analytics
from controllers.utils import Utils
from controllers.utils.dates import Dates
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()



class Performance_Dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.core = Core_Hr(dbms,object.user, object)
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.analytics =  HR_Analytics(dbms, object)
        self.total_appraisals = 0
        self.employees = []
        self.emp_list = []
        self.total_employees = 0
        self.top_emp = 0
        current_year = datetime.now().year
        first_day_last_year = datetime(current_year - 1, 1, 1)
        self.lastYearsFirstDay = first_day_last_year.strftime("%Y-%m-%d")
        self.work_plan = self.core.get_list ("Work_Plan_Task", filters={"expected_start_date__range": [self.lastYearsFirstDay, dates.get_last_date_of_current_year ()]})
        self.grouped_work_plane = self.analytics.groupbyEmp (self.work_plan)

    @classmethod
    def performance_dashboard(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        cls.get_employees(cls)
        return utils.respond(utils.ok,{
            "peformance_by_gender": cls.get_employees_by_gender(cls),
            "employees_by_department": cls.get_employees_by_department(cls),
            "employees_by_status": cls.get_employees_by_status(cls),
            "appraisals_by_type": cls.get_appraisals_by_type(cls),
            "appraisals_by_dept": cls.get_appraisal_performance_by_department(cls),
            "get_work_plan_stats_by_depts":cls.get_work_plan_stats_by_depts(cls),
            "appraisal_performance_summary_department": cls.get_appraisal_performance_by_department(cls),
            "work_plan_task_progress": cls.get_work_plan_task_progress(cls),
            "employee_attendance":cls.employee_attendance(cls)
            
        })
        
    def get_employees(self):
        employees = self.core.get_employee_list()
        top_employees = []

        def process_appraisals(appraisals):
            for data in appraisals:
                appraisee = data.appraisee
                overall_score = float(data.overall_score)
                total_closed_score = float(data.total_closed_score)
                total_open_score = float(data.total_open_score)
                employee_total_score = total_closed_score + total_open_score
                if employee_total_score > (overall_score / 2):
                    top_employees.append(appraisee)

        for emp in employees:
            employees_appraisals = self.core.get_employee_appraisals(emp.name)
            if employees_appraisals.get("appraisals"):
                process_appraisals(employees_appraisals.get("appraisals"))
            if employees_appraisals.get("self_appraisals"):
                process_appraisals(employees_appraisals.get("self_appraisals"))
        top_emp = top_employees

        if not employees:
            self.employees = []
            self.top_emp = []
        else:
            self.employees = employees
            self.top_emp = top_emp
            self.total_employees = len(self.employees)

    def get_work_plan_stats_by_depts(self):
        results = {}
        work_plan = self.dbms.get_list("Work_Plan", fetch_linked_tables=True, filters={"docstatus": 0}, privilege=True)
        if work_plan.status == utils.ok:
            work_plan_data = work_plan.data.rows

            total_tasks = 0
            completed = 0
            pending = 0
            in_Progress =  0

            for plan in work_plan_data:
                employee = plan.get('employee')
                work_plan_tasks = plan.get('work_plan_task', [])
                for task in work_plan_tasks:
                    progress_tracker = task.get('progress_tracker', "")
                    total_tasks += 1
                    if progress_tracker == "Completed":
                        completed += 1
                    elif progress_tracker == "Pending":
                            pending += 1  
                    elif progress_tracker == "In Progress":
                            in_Progress += 1
            
         
            results["completed"] = completed
            results["pending"] = pending
            results["in_progress"] = in_Progress
            results["total_tasks"] = total_tasks
        return results
            
    def employee_attendance(self):
        res = []
        hr_settings = self.core.get_company_settings (self.core.company)
        
        pp (hr_settings)
        hr_settings_working_days = 22
        
        if hr_settings and hasattr(hr_settings, 'data') and hr_settings.data.rows:
            hr_settings_data = hr_settings.data.rows[0]
            hr_settings_working_days = getattr(hr_settings_data, 'working_days', 22)
        
        emp_attendance = self.dbms.get_list("Employee_Attendance", fetch_linked_tables=True, filters={"docstatus": 0}, privilege=True)
        
        if emp_attendance.status == utils.ok:
            emp_attendance_data = emp_attendance.data.rows
            
            attendance_summary = {}
            
            for attendance in emp_attendance_data:
                employee = attendance.employee
                created_on = attendance.created_on
                year = created_on.year  
                month = created_on.month  
                month_year = f"{year}-{month:02d}"
                
                if employee not in attendance_summary:
                    attendance_summary[employee] = {}
                
                if month_year not in attendance_summary[employee]:
                    attendance_summary[employee][month_year] = 0
                
                attendance_summary[employee][month_year] += 1
            
            for employee, monthly_data in attendance_summary.items():
                for month_year, count in monthly_data.items():
                    if count == hr_settings_working_days:
                        category = "Excellent Attendance"
                        value_color = "green"
                    elif count >= hr_settings_working_days * 0.75:
                        category = "Good Attendance"
                        value_color = "light-green"
                    elif count >= hr_settings_working_days * 0.5:
                        category = "Satisfactory Attendance"
                        value_color = "yellow"
                    elif count >= hr_settings_working_days * 0.25:
                        category = "Needs Improvement"
                        value_color = "orange"
                    else:
                        category = "Poor Attendance"
                        value_color = "red"
                    
                        res.append({
                            "employee": employee,
                            "month":month_year,
                            "Attendance_count": count,
                            "Category": category,
                            "value_color":value_color
                        })
        res.sort(key=lambda x: x["Attendance_count"], reverse=True)                
        return res
    #  Good Attendance

         

   

    def get_appraisals_by_type(self):
        results = {"overall_total": 0, "appraisals": 0, "self_appraisals": 0}
        
        appraisal_setup_info = self.dbms.get_list("Appraisal_Setup", privilege=True)
        if appraisal_setup_info.status != utils.ok:
            return results
        
        for appraisal in appraisal_setup_info.data.rows:
            if appraisal['appraisal_type'] == "360 degree Appraisal":
                results["appraisals"] += 1
            elif appraisal['appraisal_type'] == "Self-Rating":
                results["self_appraisals"] += 1
        
        results["overall_total"] = results["appraisals"] + results["self_appraisals"]
        return results
    
    def get_appraisal_performance_by_department(self):
        results = {
            "values": [],
            "labels": []
        }
        
        department_scores = {}
        appraisal_quarters = set()

        try:
            # Fetch 360-degree appraisals
            appraisal_360_info = self.dbms.get_list("Appraisal", filters={"docstatus": 1}, privilege=True)
            if appraisal_360_info.status == utils.ok:
                for appraisal in appraisal_360_info.data.rows:
                    appraisal_quarter = appraisal.get("appraisal_quarter")
                    department = appraisal.get('department')
                    total_open_score = appraisal.get('total_open_score', 0)
                    total_closed_score = appraisal.get('total_closed_score', 0)
                    
                    if appraisal_quarter and department:
                        if department not in department_scores:
                            department_scores[department] = {}
                        if appraisal_quarter not in department_scores[department]:
                            department_scores[department][appraisal_quarter] = {"open": 0, "closed": 0}
                        
                        department_scores[department][appraisal_quarter]["open"] += total_open_score
                        department_scores[department][appraisal_quarter]["closed"] += total_closed_score
                        
                        appraisal_quarters.add(appraisal_quarter)
        except Exception as e:
            print(f"Error fetching 360-degree appraisals: {e}")

        try:
            # Fetch self-appraisals
            self_appraisal_info = self.dbms.get_list("Self_Appraisal", filters={"docstatus": 1}, privilege=True)
            if self_appraisal_info.status == utils.ok:
                for self_appraisal in self_appraisal_info.data.rows:
                    appraisal_quarter = self_appraisal.get("appraisal_quarter")
                    department = self_appraisal.get('department')
                    total_open_score = self_appraisal.get('total_open_score', 0)
                    total_closed_score = self_appraisal.get('total_closed_score', 0)
                    
                    if appraisal_quarter and department:
                        if department not in department_scores:
                            department_scores[department] = {}
                        if appraisal_quarter not in department_scores[department]:
                            department_scores[department][appraisal_quarter] = {"open": 0, "closed": 0}
                        
                        department_scores[department][appraisal_quarter]["open"] += total_open_score
                        department_scores[department][appraisal_quarter]["closed"] += total_closed_score
                        
                        appraisal_quarters.add(appraisal_quarter)
        except Exception as e:
            print(f"Error fetching self-appraisals: {e}")

        results["labels"] = sorted(list(appraisal_quarters))

        for department, scores in department_scores.items():
            department_data = {
                "name": department,
                "data": []
            }
            for quarter in results["labels"]:
                if quarter in scores:
                    department_data["data"].append(scores[quarter]["open"] + scores[quarter]["closed"])
                else:
                    department_data["data"].append(0)
            results["values"].append(department_data)

        return results

    def get_work_plan_task_progress(self):
        progress_stats = []

        work_plan = self.dbms.get_list("Work_Plan", fetch_linked_tables=True, privilege=True)
        if work_plan.status == utils.ok:
            work_plan_data = work_plan.data.rows

            for plan in work_plan_data:
                emp_name = plan.get('employee_name')
                total_tasks = 0
                completed_tasks = 0

                work_plan_tasks = plan.get('work_plan_task', [])
                for task in work_plan_tasks:
                    progress_tracker = task.get('progress_tracker', "")
                    total_tasks += 1
                    if progress_tracker == "Completed":
                        completed_tasks += 1

                if total_tasks > 0:
                    percentage_of_completion = (completed_tasks / total_tasks) * 100
                    progress_stats.append({
                        "employee": emp_name,
                        "percentage_of_completion": utils.fixed_decimals(percentage_of_completion, 2)
                    })

        progress_stats.sort(key=lambda x: x['percentage_of_completion'], reverse=True)

        return progress_stats
    
    def get_employees_by_department(self):
        results = {}
        mapped = {}
        departments = self.core.get_department_list()
        if len(self.emp_list) > 0:
            grouped = self.analytics.group_employees_by_department(self.emp_list, only_totals=True)
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
                results["Active"] = d.get("Active") or 0
                results["On leave"] = d.get("On Leave") or 0
                results["Left"] = 0
                if d.get("Resigned"):
                    results["Left"] += int(d.get("Resigned")) or 0
                if d.get("Terminated"):
                    results["Left"] += int(d.get("Terminated")) or 0
        return results
    


    def get_employees_by_gender(self):
        results = utils.from_dict_to_object ({"Male": 0, "Female": 0})
        if self.grouped_work_plane and self.grouped_work_plane.by_emp and len (self.grouped_work_plane.by_emp) > 0:
            for emp in self.grouped_work_plane.by_emp:
                employee = self.core.get_doc ("Employee", emp.planer_of_work_plan)
                if employee and str (employee.gender).lower () == "male":
                    results.Male += int (emp.completed)
                elif employee and str (employee.gender).lower () == "female":
                    results.Female += int (emp.completed)
        return results