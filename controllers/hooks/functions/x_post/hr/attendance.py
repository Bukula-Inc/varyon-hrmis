from  controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from datetime import date, datetime

utils = Utils ()
dates = Dates ()

pp = utils.pretty_print
throw = utils.throw

def take_attendance (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    status = utils.unprocessable_entity
    res = "Failed To Take Attendance"
    obj = object.body.data
    emp = core_hr.get_doc ("Employee", obj.confirm_employee_id)
    if emp:
        check_today_attendance = core_hr.get_list ("Employee_Attendance", filters= {
            "attendance_date": dates.today (),
            "employee": emp.name,
        })
        if check_today_attendance:
            res = f"Attendance {emp.full_name} Already Taken"
        else:
            att = utils.from_dict_to_object ({
                "attendance_date": dates.today (),
                "shift": "Day",
                "department": emp.department,
                "designation": emp.designation,
                "employee_name": emp.full_name,
                "employee": emp.name,
                "company": emp.company,
                "manager": emp.reports_to,
                "time_in": datetime.now().time(),
            })

            r = dbms.create ("Employee_Attendance", att, submit_after_create=True)
            if r.status == utils.ok:
                status = utils.ok

    return utils.respond (status, res)