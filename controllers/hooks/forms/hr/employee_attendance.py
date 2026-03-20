from django.utils import timezone
from controllers.utils import Utils 
from controllers.core_functions.hr import Core_Hr
utils = Utils ()
pp = utils.pretty_print

def employee_attendance_in (dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    att = core_hr.get_list ("Employee_Attendance", filters={"employee": object.body.employee, "employee_name": object.body.employee_name, "attendance_date": object.body.attendance_date}, limit=1)
    if att:
        utils.throw (f"{object.body.employee_name} Attendance Already Taken")
    object.body.time_in  = timezone.now ()

def employee_attendance_out (dbms, object):
    object.body.time_out  = timezone.now ()