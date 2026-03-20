from controllers.utils import Utils
from controllers.utils.dates import Dates

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def back_from_leave(dbms, object):
    emp_lst =None
    emp_list =None

    to_date =dates.add_days(dates.today(), -1)

    fetch_leave =dbms.get_list("Leave_Application", filters={"to_date": to_date})
    if fetch_leave.status ==utils.ok:
        leave_lst =fetch_leave.data.rows
        emp_lst =[leave.employee for leave in leave_lst]
        pp(leave_lst)
        
    if emp_lst != None:
        fetch_employee =dbms.get_list("Employee", filters={"name__in": emp_lst},)
        if fetch_employee.status ==utils.ok:
            emp_list =fetch_employee.data.rows
    
    if emp_list !=None:
        for emp in emp_list:
            emp.status ="Active"
            try:
                dbms.update("Employee", emp)
            except Exception as e:
                pp(e)

    return utils.respond(utils.ok, {"condition": "Done"})