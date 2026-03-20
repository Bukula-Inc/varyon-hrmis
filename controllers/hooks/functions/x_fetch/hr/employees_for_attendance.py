from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

utils =Utils()
dates = Dates ()
pp =utils.pretty_print
throw =utils.throw

def employees_for_attendance(dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    status = utils.not_found
    res = {"status": status, "error_message": "employees Found"}
    emp_data =[]
    get_emps = core_hr.get_list("Employee", filters={"status": "Active"})
    if get_emps:
        res = "Success"
        status = utils.ok
        for emp in get_emps:
            check_today = core_hr.get_list("Employee_Attendance", filters={
                "attendance_date": dates.today (),
                "employee": emp.name,
            })
            if check_today:
                emp.attended = True
            emp_data.append (emp)
        res = emp_data
    return utils.respond(status, res)