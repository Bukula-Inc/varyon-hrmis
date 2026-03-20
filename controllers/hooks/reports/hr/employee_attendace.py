from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import date, datetime
import calendar

utils =Utils()
dates =Dates()
pp =utils.pretty_print

def monthly_attendance(dbms, object):
    return_data =[]
    filters =object.filters
    fetch_attendance =dbms.get_list("Employee_Attendance", filters=filters)
    for attendance in fetch_attendance.data.rows:

          return_data.append(utils.from_dict_to_object({ 
            "posting_date": attendance.attendance_date or None,
            "employee_id": attendance.employee or None,
            "employee_full_name": attendance.employee_name or None,
            "day":  attendance.attendance_date.strftime("%A") if isinstance(attendance.attendance_date, date or datetime) else (datetime.strptime(attendance.attendance_date, "%Y-%m-%d")).strftime("%A"),
            "time_in": attendance.time_in or None,
            "time_out": attendance.time_out or None,  
           }))

    return utils.respond(utils.ok, {"rows" :return_data})
