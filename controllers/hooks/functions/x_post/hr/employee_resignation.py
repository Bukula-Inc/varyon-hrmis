from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

utils = Utils()
dates = Dates ()
throw = utils.throw
pp = utils.pretty_print


def employee_resignation(dbms, object):
    employee_resignation = dbms.get_doc("employee_separation",object.body.data.id, user=object.user)
    if employee_resignation.get("status") != utils.ok:
        return employee_resignation
    data = (employee_resignation.get("data"))
    data.status = "Comfirmed"
    update = dbms.update("employee_separation", data, object.user, update_submitted=True)
    return update


def separate_with_separated_employees (dbms, object):
    core_hr = Core_Hr (dbms)
    employee_dict = utils.from_dict_to_object ()
    employee = core_hr.get_employee_list (filters={"is_separated": 1})
    if employee:
        employee_dict = utils.array_to_dict (employee, "name")
    msg = "Successfully Separated"
    separation_type = DataConversion.safe_get (object.body.data, "separation_type", None)
    emps = DataConversion.safe_get(object.body.data, "employees", [])
    len_emps = len (emps)
    worked_emp = 0
    for emp in emps:
        employee = DataConversion.safe_get (employee_dict, DataConversion.safe_get (emp, "name", None), None)
        if employee:
            ldw = DataConversion.safe_get (emp, "last_day_of_work", None)
            separation_obj = utils.from_dict_to_object ({
                "employee_name": DataConversion.safe_get (emp, "full_name", None) or DataConversion.safe_get (employee, "full_name", None),
                "employee": DataConversion.safe_get (emp, "name", None),
                "separation_type": separation_type,
                "department": DataConversion.safe_get (employee, "department", None),
                "designation": DataConversion.safe_get (employee, "designation", None),
                "reports_to": DataConversion.safe_get (employee, "reports_to", None),
                "last_day_of_work": ldw if ldw else DataConversion.safe_get (employee, "last_day_of_work", None),
                "skip_exit_interview": 1,
                "skip_final_statement": 1,
                "resignation_date": dates.today (),
                "notice_period": None,
                "notify_users": None,
                "activities": None,
                "reason": "Separating Already Separated Employees to Normalize the Employees Data"
            })
            r = dbms.create ("Employee_Seperation", separation_obj, skip_workflows=True, submit_after_create=True)
            if r.status == utils.ok:
                worked_emp += 1
    if (len_emps - worked_emp) <= 0:
        msg = "Failed To Separate"

    return utils.respond (utils.ok, msg)