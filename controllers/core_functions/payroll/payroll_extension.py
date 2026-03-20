from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.payroll import Core_Payroll
import pandas as pd

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class Payroll_Extension:
    def __init__(self,dbms, obj=None):
        self.dbms = dbms
        self.obj = obj
        self.core_payroll = Core_Payroll (self.dbms)

    def __get_employee_profile(self, user_name):
        employee = self.dbms.get_list("Employee", filters={"user": user_name}, privilege=True)
        utils.evaluate_response(employee, f"An error occurred while fetching employee: {employee.error_message}")
        if len(employee.data.rows) > 1:
            throw("This user is linked to more than one employee profiles")
        employee = employee.data.rows[0]
        return utils.from_dict_to_object({
            "id": employee.id,
            "name": employee.name,
            "status": employee.status,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "middle_name": employee.middle_name,
            "full_name": employee.full_name,
            "gender": employee.gender,
            "dob": employee.d_o_b,
            "salutation": employee.salutation,
            "id_no": employee.id_no,
            "nhima": employee.nhima,
            "napsa": employee.napsa,
            "tpin": employee.tpin,
            "doj": employee.date_of_joining,
            "email": employee.email,
            "contact_no": employee.contact,
            "supervisor": employee.report_to,
            "working_days": employee.working_days,
            "working_hours": employee.working_hours,
            "company": employee.company,
            "designation": employee.designation,
            "branch": employee.branch,
            "department": employee.department,
            "status_color": employee.status_color,
            "status_inner_color": employee.status_inner_color
        })

    def get_staff_payroll_related_stats(self, user_name):
        try:
            if not user_name:
                throw("User Name is required")
            employee = self.__get_employee_profile(user_name)
            pay_stats = self.pay_history (employee.name, user_name)
            return pay_stats
        except Exception as err:
            pp (f"Error in get Payroll Status: {err}")
            pass

    def pay_history (self, employee=None, user_name=None):
        try:
            filters = utils.from_dict_to_object ()
            recent_payslips = []
            totals = {
                "basic_pay": 0.00,
                "gross": 0.00,
                "total_deductions": 0.00,
                "net": 0.00,
                "advance_amount": 0.00,
                "advance_repaid": 0.00,
                "overtime": 0.00
            }
            if employee:
                filters.employee = employee
            get_payslips = self.core_payroll.get_list ("Payslip", filters=filters, order_by=['-to_date'])
            if get_payslips:
                df = utils.to_data_frame (get_payslips)
                fields_to_sum = [
                    "basic_pay",
                    "gross",
                    "total_deductions",
                    "net",
                    "advance_amount",
                    "advance_repaid",
                    "overtime"
                ]
                df[fields_to_sum] = df[fields_to_sum].apply(pd.to_numeric, errors="coerce").fillna(0)
                totals = df[fields_to_sum].sum().to_dict()
                totals = utils.from_dict_to_object ({k: round(v, 2) for k, v in totals.items()})
                recent_payslips = get_payslips[:3]
            return {
                "ytd_summary": totals,
                "recent_payslip": recent_payslips,
                "advance_amount": DataConversion.convert_to_float (DataConversion.safe_get (totals, "advance_amount", 0) - DataConversion.safe_get (totals, "advance_repaid", 0)),
                "advance_repaid": DataConversion.convert_to_float (DataConversion.safe_get (totals, "advance_repaid", 0)),
            }

        except Exception as err:
            pp (f"Error in get Pay History: {err}")
            pass

        # body = self.object.body
        # owner = self.dbms.get_doc("Lite_User", body.work_plan_for or self.dbms.current_user.name, privilege=True)
        # utils.evaluate_response(owner, f"Failed to fetch work plan owner:{owner.error_message}")
        # owner = owner.data
        # employee = self.dbms.get_list("Employee", filters={"user":owner.name}, privilege=True)
        # if employee.status == utils.ok:
        #     if len(employee.data.rows) > 1:
        #         throw("This user account is linked to more than one employee profiles!")
        #     employee = employee.data.rows[0]
        # else:
        #     employee = utils.from_dict_to_object()
        # if not body.period:
        #     body.period = "Daily"
        # if not utils.get_text_from_html_string(body.goals_and_objectives):
        #     throw("Please enter your goals and objectives for this task!")
        # if body.period == "Hourly":
        #     if not body.commencement_time:
        #         throw("For Hourly Workplan, Commencement Time is mandatory!")
        # elif body.period == "Daily":
        #     if not body.commencement_date:
        #         throw("For Daily Work plan, Commencement Date is mandatory!")
        # elif body.period == "Monthly":
        #     if not body.month:
        #          throw("For Monthly Work plan, Month selection is mandatory!")    
        # elif body.period == "Quarterly":
        #     if not body.month:
        #          throw("For Quarterly Work plan, Quarter selection is mandatory!")
        # if not body.work_plan_task or len(body.work_plan_task) <= 0:
        #     throw("Add at least one task to this work plan")
        
       
        # body.full_name = f"{owner.first_name} {owner.middle_name or ''} {owner.last_name}"
        # body.work_plan_for = owner.name
        # body.commencement_date = body.commencement_date or dates.today()
        # body.employee = employee.name
        # body.company = employee.company or self.dbms.current_user.default_company

        # # validate tasks
        # body.total_tasks = len(body.work_plan_task)
        # body.overdue_tasks = 0
        # body.open_tasks = 0
        # body.closed_tasks = 0
        # for idx, task in enumerate(body.work_plan_task):
        #     if not task.title:
        #         throw(f"Please give task '{idx +1}' a title!")
        #     if not utils.get_text_from_html_string(task.description):
        #         throw(f"Please describe task '{idx +1}'")
        #     if not task.expected_start_date:
        #         task.expected_start_date = dates.today()
        #     if not task.expected_completion_date:
        #         task.expected_completion_date = dates.add_days(dates.today(), 1)
        #     if body.period == "Hourly":
        #         if not task.expected_start_time or not task.expected_completion_time:
        #             throw(f"For Hourly Work plan, Expected Start Time & Expected Completion Time is mandatory for task {idx +1}!")
        #     if body.period == "Daily":
        #         if not task.expected_start_date or not task.expected_completion_date:
        #             throw(f"For Daily Work plan, Expected Start Date & Expected Completion Date is mandatory for task {idx +1}!")

        #     if task.task_status in ["Pending", "Active", "Open"]:
        #         body.open_tasks += 1
        #     elif task.task_status in ["Closed", "Completed"]:
        #         body.completed_tasks += 1