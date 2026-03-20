from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr
from datetime import datetime
import numpy as np
import pandas as pd

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class HR_Extension:
    def __init__(self,dbms, object=None):
        self.dbms = dbms
        self.object = object
        self.hr = Core_Hr (self.dbms)


    # emploee profile dashboard stats
    def __get_employee_profile(self, user_name):
        employee = self.hr.get_list("Employee", filters={"user": user_name}, privilege=True)
        if not employee:
            throw (f"An error occurred while fetching employee")
        if employee and len(employee) > 1:
            throw("This user is linked to more than one employee profiles")
        employee = employee[0]
        return utils.from_dict_to_object({
            "id": DataConversion.safe_get (employee, "id"),
            "name": DataConversion.safe_get (employee, "name"),
            "status": DataConversion.safe_get (employee, "status"),
            "first_name": DataConversion.safe_get (employee, "first_name"),
            "last_name": DataConversion.safe_get (employee, "last_name"),
            "middle_name": DataConversion.safe_get (employee, "middle_name"),
            "full_name": DataConversion.safe_get (employee, "full_name"),
            "gender": DataConversion.safe_get (employee, "gender"),
            "dob": DataConversion.safe_get (employee, "d_o_b"),
            "salutation": DataConversion.safe_get (employee, "salutation"),
            "id_no": DataConversion.safe_get (employee, "id_no"),
            "nhima": DataConversion.safe_get (employee, "nhima"),
            "napsa": DataConversion.safe_get (employee, "napsa"),
            "tpin": DataConversion.safe_get (employee, "tpin"),
            "doj": DataConversion.safe_get (employee, "date_of_joining"),
            "basic": DataConversion.convert_to_float (DataConversion.safe_get (employee, "basic_pay")),
            "email": DataConversion.safe_get (employee, "email"),
            "contact_no": DataConversion.safe_get (employee, "contact"),
            "supervisor": DataConversion.safe_get (employee, "report_to"),
            "working_days": DataConversion.safe_get (employee, "working_days"),
            "working_hours": DataConversion.safe_get (employee, "working_hours"),
            "company": DataConversion.safe_get (employee, "company"),
            "designation": DataConversion.safe_get (employee, "designation"),
            "branch": DataConversion.safe_get (employee, "branch"),
            "department": DataConversion.safe_get (employee, "department"),
            "status_color": DataConversion.safe_get (employee, "status_color"),
            "status_inner_color": DataConversion.safe_get (employee, "status_inner_color")
        })

    def __get_employee_files(self, employee_name, user_name):
        files = []
        try:
            if employee_name:
                files_data = self.hr.get_list ("Employee_File", filters={"employee": employee_name}, fetch_linked_tables=True, privilege=True, limit=1)
                if files_data:
                    files = DataConversion.safe_get (files_data[0], 'file_content', files)
            return files
        except Exception as err:
            pp (f"Error in get employee files: {err}")
            pass

    def get_staff_hr_related_stats(self, user_name):
        if not user_name:
            throw("User Name is required")
        employee = self.__get_employee_profile(user_name)
        files = self.__get_employee_files(employee.name, user_name)
        leave_info = self.__leave_data (employee, user_name)
        work_plan = self.__work_plan (employee.name, user_name)
        return utils.from_dict_to_object({
            "employee_info": employee,
            "employee_files": files,
            "leave_info": leave_info,
            "work_plan": work_plan,
        })

    def __work_plan (self, employee, username):
        try:
            summary = utils.from_dict_to_object ({
                "completed": 0,
                "total": 0,
                "pending": 0,
                "overdue": 0,
            })
            today = utils.from_dict_to_object ({
                "total_tasks": 0,
                "completed": 0,
                "tasks": []
            })
            # , filters={"status": "Active", "employee": employee}
            work_plan = self.hr.get_list ("Work_Plan", fetch_linked_tables=True)
            if work_plan:
                work_plan_task = DataConversion.safe_get (work_plan[0], "work_plan_task", [])
                summary.total = len (work_plan_task)
                for task in work_plan_task:
                    pp (task)
                    task_status = DataConversion.safe_get (task, "task_status", '')
                    if DataConversion.safe_get (task, "expected_start_date", datetime.today ()) == datetime.today ():
                        today.total_tasks += 1
                        if str (task_status).lower () == "completed":
                            today.completed += 1
                        today.tasks.append (task)
                    if str (task_status).lower () == "pending":
                        if DataConversion.safe_lt (DataConversion.safe_get (task, "expected_completion_date", datetime.today ()), datetime.today (), datatype=datetime):
                            summary.overdue += 1
                        else:
                            summary.pending += 1

                    elif str (task_status).lower () == "completed":
                        summary.completed += 1
                    elif str (task_status).lower () == "in progress":
                        if DataConversion.safe_lt (DataConversion.safe_get (task, "expected_completion_date", datetime.today ()), datetime.today (), datatype=datetime):
                            summary.overdue += 1
            return {
                "summary": summary,
                "today": today,
            }
        except Exception as err:
            pp (f"Error in Work Plan: {err}")
            pass


    def __leave_data (self, employee, user_name):
        try:
            return_dict = utils.from_dict_to_object ()
            applications_stats = "0/0"
            leave_days_sats = self.hr.emp_get_leave_value (employee.id, employee.working_days, basic=employee.basic)
            apps = []
            days = []
            labels = []
            if employee:
                leave_balance_list = self.hr.get_list ("Leave_Entry", filters={"employee": employee})
                leave_apps = self.hr.get_list ("Leave_Application", filters={"employee": employee, "leave_type": "Annual Leave", })
                if leave_balance_list:
                    grouped_entries = utils.to_data_frame (leave_balance_list)
                    grouped_entries.replace({np.nan: 0, None: 0})
                    cur_entry = grouped_entries[grouped_entries['is_active'] == 1].to_dict("records")
                    if len (cur_entry) > 0:
                        cur_entry = cur_entry[0]
                    else:
                        cur_entry = {}
                    grouped_entries['created_on'] = pd.to_datetime(grouped_entries['created_on'])
                    grouped_entries['month'] = grouped_entries['created_on'].dt.strftime('%b')
                    nested_group = (
                        grouped_entries.groupby(['entry_type', 'month'])
                        .apply(lambda x: x.to_dict("records"))
                        .unstack(fill_value=[])
                        .to_dict()

                    )
                    labels = list(nested_group.keys())
                    for label in labels:
                        monthly_applications = []
                        month_allocations = []
                        label_data = DataConversion.safe_get (nested_group, label, {})
                        apps_ = DataConversion.safe_get (label_data, "Application", [])
                        allocs = DataConversion.safe_get (label_data, "Allocation", [])
                        df_apps = utils.to_data_frame (apps_)
                        df_allocs = utils.to_data_frame (allocs)
                        if apps_:
                            monthly_applications = df_apps.groupby ("leave_type").agg ({
                                "used_leave_days": 'sum'
                            }).to_dict (orient="records")
                        if allocs:
                            month_allocations = df_allocs.groupby ("leave_type").agg ({
                                "remaining_leave_days": 'sum'
                            }).to_dict (orient="records")
                        if len (monthly_applications) > 0:
                            apps.append (DataConversion.safe_get(monthly_applications[0], "used_leave_days", 0))
                        if len (month_allocations) > 0:
                            days.append (DataConversion.safe_get(month_allocations[0], "remaining_leave_days", 0))

                if leave_apps:
                    leave_df = utils.to_data_frame (leave_apps)
                    leave_df = leave_df.replace({np.nan: 0, None: 0})
                    approved = leave_df[leave_df['approved'] == 1].to_dict("records")
                    unapproved = leave_df[leave_df['approved'] == 0].to_dict("records")
                    leave_status = {
                        "approved": approved,
                        "unapproved": unapproved
                    }

                    applications_stats = f"{len(DataConversion.safe_get (leave_status, 'approved', []))}/{len (leave_apps)}"
                return_dict = utils.from_dict_to_object ({
                    "balance": DataConversion.safe_get (leave_days_sats, "remaining_days"),
                    "leave_stats": applications_stats,
                    "leave_status": {
                        "labels": labels,
                        "days": days,
                        "apps": apps,
                    }
                })
            return return_dict
        except Exception as err:
            pp (f"Error in get employee LEave: {err}")
            pass



    def generate_work_plan(self):
        body = self.object.body
        owner = self.dbms.get_doc("Lite_User", body.work_plan_for or self.dbms.current_user.name, privilege=True)
        utils.evaluate_response(owner, f"Failed to fetch work plan owner:{owner.error_message}")
        owner = owner.data
        employee = self.dbms.get_list("Employee", filters={"user":owner.name}, privilege=True)
        if employee.status == utils.ok:
            if len(employee.data.rows) > 1:
                throw("This user account is linked to more than one employee profiles!")
            employee = employee.data.rows[0]
        else:
            employee = utils.from_dict_to_object()
        if not body.period:
            body.period = "Daily"
        if not utils.get_text_from_html_string(body.goals_and_objectives):
            throw("Please enter your goals and objectives for this task!")
        if body.period == "Hourly":
            if not body.commencement_time:
                throw("For Hourly Workplan, Commencement Time is mandatory!")
        elif body.period == "Daily":
            if not body.commencement_date:
                throw("For Daily Work plan, Commencement Date is mandatory!")
        elif body.period == "Monthly":
            if not body.month:
                throw("For Monthly Work plan, Month selection is mandatory!")    
        elif body.period == "Quarterly":
            if not body.month:
                throw("For Quarterly Work plan, Quarter selection is mandatory!")
        if not body.work_plan_task or len(body.work_plan_task) <= 0:
            throw("Add at least one task to this work plan")
        body.full_name = f"{owner.first_name} {owner.middle_name or ''} {owner.last_name}"
        body.work_plan_for = owner.name
        body.commencement_date = body.commencement_date or dates.today()
        body.employee = employee.name
        body.company = employee.company or self.dbms.current_user.default_company

        # validate tasks
        body.total_tasks = len(body.work_plan_task)
        body.overdue_tasks = 0
        body.open_tasks = 0
        body.closed_tasks = 0
        for idx, task in enumerate(body.work_plan_task):
            if not task.title:
                throw(f"Please give task '{idx +1}' a title!")
            if not utils.get_text_from_html_string(task.description):
                throw(f"Please describe task '{idx +1}'")
            if not task.expected_start_date:
                task.expected_start_date = dates.today()
            if not task.expected_completion_date:
                task.expected_completion_date = dates.add_days(dates.today(), 1)
            if body.period == "Hourly":
                if not task.expected_start_time or not task.expected_completion_time:
                    throw(f"For Hourly Work plan, Expected Start Time & Expected Completion Time is mandatory for task {idx +1}!")
            if body.period == "Daily":
                if not task.expected_start_date or not task.expected_completion_date:
                    throw(f"For Daily Work plan, Expected Start Date & Expected Completion Date is mandatory for task {idx +1}!")

            if task.task_status in ["Pending", "Active", "Open"]:
                body.open_tasks += 1
            elif task.task_status in ["Closed", "Completed"]:
                body.completed_tasks += 1