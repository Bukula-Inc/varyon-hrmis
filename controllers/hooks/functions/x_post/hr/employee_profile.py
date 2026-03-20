from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.dates import Dates

dates = Dates ()

utils = Utils ()
throw = utils.throw
pp = utils.pretty_print

class Employee_Profile:
    def __init__ (self, dbms, object) -> None:
        self.dbms = dbms
        self.core_hr = Core_Hr (dbms=dbms)
        if not object.body.data.emp_id:
            self.employee = None
        self.employee = object.body.data.emp_id

    def check_float (self, float_data):
        return float_data if float_data else '0.00'
    
    def years_saved (self, start_date, to_date= None):
        if to_date:
            dates.date_difference(start_date, to_date, unit="years")
    
    def get_leave_applications (self, emp):
        applications = self.core_hr.get_list ("Leave_Application", filters={"employee": emp}, order_by="-id")
        pp (applications)
        if applications:
            return applications[-5:]
        return []

    @classmethod
    def employee_profile (cls, dbms, object):
        cls = cls (dbms, object)
        if not cls.employee:
            return utils.respond (utils.no_content, response="Unknown Employees")
        employee = cls.core_hr.get_employee (
            employee_id=cls.employee,
            get_payslip_analytics=True,
            get_leave_days=True,
            get_advance=True,
            get_overtime=True,
            get_work_plan=True,
        )
        if employee.status == utils.ok:
            emp = employee.data
        else:
            emp = cls.core_hr.get_doc ("Employee", cls.employee)
        if not emp:
            return utils.respond (utils.no_content, response="Unknown Employees")
        deductions = emp.deductions

        return utils.respond (utils.ok, {
            "employee": {
                "full_name": emp.full_name,
                "supervisor": emp.report_to,
                "job_title": emp.designation,
                "company": emp.company,
                "department": emp.department,
                "email": emp.email,
                "contact": emp.contact,
                "emergency": emp.contact,
                "status": emp.status,
                "joining_date": emp.date_of_joining,
                "dob": emp.d_o_b,
                "basic_pay": emp.basic_pay,
                "currency": emp.currency,
            },
            "leave_applications": cls.get_leave_applications (cls.employee),
            "work_plan": emp.work_plan,
            "leave_summary": emp.leave_summary,
            "top_cards": {
                "leave": {
                    "leave_days": emp.payslip_analytics.overall_current_leave_days,
                    "leave_value": cls.check_float (emp.payslip_analytics.overall_current_leave_value)
                },
                "years_served": cls.years_saved (emp.date_of_joining)
            }
        })