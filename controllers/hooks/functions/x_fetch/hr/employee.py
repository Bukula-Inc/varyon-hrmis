import pandas as pd
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion

dates = Dates ()
utils = Utils ()
pp = utils.pretty_print

def get_separated_employees (dbms, object):
    return_data = []
    core_hr = Core_Hr (dbms=dbms)
    emps = core_hr.get_employee_list (filters={"is_separated": 1}, fields=["name", "first_name", "middle_name", "last_name", "full_name", "last_day_of_work"])
    if emps:
        return_data = emps
    return utils.respond (utils.ok, return_data)

def get_employees_for_profile (dbms, object):
    return_data = []
    core_hr = Core_Hr (dbms=dbms)
    emps = core_hr.get_employee_list (filters={"status__in": ["Active", "On Leave", "Suspended"]}, fields=["name", "first_name", "middle_name", "last_name", "full_name"])
    if emps:
        return_data = emps
    return utils.respond (utils.ok, return_data)

def get_salary_components (dbms, object):
    core = Core_Hr (dbms=dbms)
    salary_components = core.get_list ("Salary_Component", filters={"is_statutory_component": 1})
    if salary_components:
        return utils.respond (status=utils.ok, response=salary_components)
    return utils.respond (status=utils.no_content, response={"status": utils.no_content, "error_message": "No Statutory Components Found"})


def get_training_program_summary(dbms, object):
    info = dbms.get_list("Training_Program", privilege=True, fetch_linked_tables=False)
    status_counts = {
        "Draft": 0,
        "Pending_Approval": 0,
        "Approved": 0,
        "Rejected": 0,
        "Total": 0,
    }

    if info["status"] == utils.ok:
        info = info["data"]["rows"]

        for doc in info:
            status_counts[doc["status"]] += 1

        status_counts["Total"] = status_counts["Draft"] + status_counts["Pending_Approval"] + status_counts["Approved"] + status_counts["Rejected"] 

    return utils.respond (status=utils.ok, response=status_counts)

def deactivate_separated_employees (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    employees = core_hr.get_list ("Employee", filters={"status__in": ["Separated", "Terminated", "Redundant", "Retired", "Resigned", "Left"], "is_separated": 0}) 
    if employees:
        for emp in employees:
            emp.is_separated = 1
            dbms.update ("Employee", emp, update_submitted=True)
        return utils.respond (utils.ok, "Success")
    return utils.respond (utils.not_found, "Failed")

def alter_employee_pay (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    get_all_emps = core_hr.get_employee_list ()
    processed = 0
    if get_all_emps and len (get_all_emps) > 0:
        for emp in get_all_emps:
            emp_salary = utils.from_dict_to_object ({
                "employee": emp.name,
                "basic_pay": emp.basic_pay,
                "tax_band": emp.tax_band,
                "employee_grade": emp.employee_grade,
                "earnings": emp.earnings,
                "deductions": emp.deductions,
                "is_current": 1,
                "promoted": 0,
                "working_days": emp.working_days,
                "working_hours": emp.working_hours,
                "currency": emp.currency,
                "employment_status": "Employed"
            })
            r = dbms.create ("Employee_Pay_And_Salary", emp_salary,)
            if r.status == utils.ok:
                emp.employee_saved = 0
                emp.full_name = f"{emp.first_name} {emp.middle_name or ''} {emp.last_name}"
                r = dbms.update ("Employee", emp)
                pp (r)
                processed += 1

    return utils.respond (status=utils.ok, response=f"Process Completed. Processed {processed} Employees")


def normalize_emp_information (dbms, object):
    core_hr = Core_Hr (dbms)
    hr_ss = core_hr.get_company_settings (core_hr.company)
    working_hours = DataConversion.safe_get (hr_ss, 'working_hrs', 8)
    working_days = DataConversion.safe_get (hr_ss, 'working_days', 22)
    employees = core_hr.get_list ("Employee", {"status__in": ["Active", 'On Leave', "Suspended", "Draft"]})
    success = 0
    failed = 0
    if employees:
        
        for emp in employees:
            if emp:
                DataConversion.safe_set (emp, "salutation", "")
                DataConversion.safe_set (emp, "last_day_of_work", dates.add_days (dates.today (), 23741))
                DataConversion.safe_set (emp, "create_user", None)
                DataConversion.safe_set (emp, "email", "")
                DataConversion.safe_set (emp, "probation", "")
                DataConversion.safe_set (emp, "employee_saved", 1)
                DataConversion.safe_set (emp, "report_to", '')
                DataConversion.safe_set (emp, "leave_approver", '')
                DataConversion.safe_set (emp, "shift_approver", '')
                DataConversion.safe_set (emp, "requisition", '')
                DataConversion.safe_set (emp, "bank_name", '')
                DataConversion.safe_set (emp, "account_no", '')
                DataConversion.safe_set (emp, "sort_code", '')
                DataConversion.safe_set (emp, "create_user", '')
                DataConversion.safe_set (emp, "end_of_contract", dates.add_days (dates.today (), 23741))
                DataConversion.safe_set (emp, "contract", '')
                DataConversion.safe_set (emp, "user", None)
                DataConversion.safe_set (emp, "tax_band", "PAYE")
                DataConversion.safe_set (emp, "currency", '')
                
                status = DataConversion.safe_get (emp, "status")
                if not DataConversion.safe_get (emp, "full_name"):
                    DataConversion.safe_set (emp, "full_name", f"{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}")
                if DataConversion.safe_get (emp, "inable_probation") != 1:
                    DataConversion.safe_set (emp, "inable_probation", 0)
                if DataConversion.safe_get (emp, "is_separated") != 1:
                    DataConversion.safe_set (emp, "is_separated", 0)
                if not DataConversion.safe_get (emp, "is_separated_emp_paid"):
                    DataConversion.safe_set (emp, "is_separated_emp_paid", "Unsettled")
                if status == "Draft":
                    DataConversion.safe_set (emp, "status", "Active")
                # if not DataConversion.safe_get (emp, "working_days"):
                DataConversion.safe_set (emp, "working_days", working_days)
                # if not DataConversion.safe_get (emp, "working_hours"):
                DataConversion.safe_set (emp, "working_hours", working_hours)
                DataConversion.safe_set (emp, "employee_saved", 1)
                r = dbms.update ("Employee", emp, update_submitted=True)
                pp (emp.name, emp.full_name, r)
                if r.status != utils.ok:
                    pp (emp)
                    failed += 1
                    break
                else:
                    success += 1
    pp (f"SUCCESS: {success} =>> FAID: {failed}")
    return utils.respond (utils.ok, "done")


def add_paye_to_all_employees (dbms, object):
    core_hr = Core_Hr (dbms)
    employees = core_hr.get_list ("Employee", {"status__in": ["Active", 'On Leave', "Suspended"]})
    if employees:
        for emp in employees:
            if not DataConversion.safe_get (emp, "tax_band"):
                DataConversion.safe_set (emp, "tax_band", "PAYE")
                r = dbms.update ("Employee", emp, update_submitted=True)
    return utils.respond (utils.ok, "done")
